import base64
from typing import Any
from typing import List
from typing import Optional

import requests
from evmosgrpc.accounts import get_account_all_balances
from evmosgrpc.broadcaster import broadcast
from evmosgrpc.builder import ExternalWallet
from evmosgrpc.constants import CHAIN_ID
from evmosgrpc.constants import FEE
from evmosgrpc.constants import GAS_LIMIT
from evmosgrpc.messages.msgsend import create_msg_send
from evmosgrpc.transaction import create_tx_raw
from evmosgrpc.transaction import Transaction
from evmoswallet.eth.ethereum import sha3_256
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from google.protobuf.json_format import MessageToDict
from pydantic.main import BaseModel
from sqlalchemy.orm import Session
from src.constants import REST_ENDPOINT
from src.database import session_for_request
from src.endpoints.constants import BLOCKCHAIN_TAG

router = APIRouter()


# Schemas
class Coin(BaseModel):
    denom: str
    amount: int


class Balances(BaseModel):
    balances: List[Coin]


@router.get('/balance/{user_wallet}', tags=[BLOCKCHAIN_TAG], response_model=Balances)
async def get_balance(user_wallet: str, db: Session = Depends(session_for_request)):
    ret = []
    try:
        res = get_account_all_balances(user_wallet)
        ret = res['balances']
    except Exception as e:
        print(e)
        # Invalid wallet / no balance
        pass
    return {'balances': ret}


# Schemas
class MessageData(BaseModel):
    bodyBytes: str
    authInfoBytes: str
    chainId: str
    accountNumber: int
    signBytes: str


class Wallet(BaseModel):
    address: str
    algo: str
    pubkey: str


class MsgSend(BaseModel):
    wallet: Wallet
    amount: int
    destination: str
    denom: str
    memo: str


class BroadcastData(BaseModel):
    bodyBytes: str
    authBytes: str
    signature: str


class ClaimsRequest(BaseModel):
    address: str


class Claim(BaseModel):
    action: str
    completed: bool
    claimable_amount: str


class ClaimsData(BaseModel):
    initial_claimable_amount: str
    claims: List[Claim]


class ClaimsResponse(BaseModel):
    data: Optional[ClaimsData]
    error: Optional[str]


def generate_message(tx: Transaction,
                     builder: ExternalWallet,
                     msg: Any,
                     memo: str = '',
                     fee: str = FEE,
                     gas_limit: str = GAS_LIMIT):
    tx.create_tx_template(builder, msg, memo=memo, fee=fee, gas_limit=gas_limit)

    to_sign = tx.create_sig_doc()
    bodyBytes = base64.b64encode(tx.body.SerializeToString())
    authInfoBytes = base64.b64encode(tx.info.SerializeToString())
    chainId = CHAIN_ID
    accountNumber = int(builder.account_number)
    return {
        'bodyBytes': bodyBytes,
        'authInfoBytes': authInfoBytes,
        'chainId': chainId,
        'accountNumber': accountNumber,
        'signBytes': base64.b64encode(sha3_256(to_sign).digest())
    }


@router.post('/msg_send', response_model=MessageData)
def create_msg(data: MsgSend):
    builder = ExternalWallet(
        data.wallet.address,
        data.wallet.algo,
        base64.b64decode(data.wallet.pubkey),
    )
    tx = Transaction()
    msg = create_msg_send(
        builder.address,
        data.destination,
        data.amount,
        denom=data.denom,
    )
    return generate_message(tx, builder, msg)


@router.post('/broadcast')
def signed_msg(data: BroadcastData):
    raw = create_tx_raw(
        body_bytes=base64.b64decode(data.bodyBytes),
        auth_info=base64.b64decode(data.authBytes),
        signature=base64.b64decode(data.signature),
    )
    result = broadcast(raw)
    dictResponse = MessageToDict(result)
    print(dictResponse)
    if 'code' in dictResponse['txResponse'].keys():
        return {'res': False, 'msg': dictResponse['txResponse']['rawLog']}
    return {'res': True, 'msg': dictResponse['txResponse']['txhash']}


@router.post('/claims')
def claims(data: ClaimsRequest):
    r = requests.get(f'{REST_ENDPOINT}evmos/claims/v1/claims_records/{data.address}')
    if r.status_code == 200:
        resp = r.json()
        return ClaimsResponse(data=resp)
    elif r.status_code == 404:
        # Wallet not in the claims database
        actions = []
        for action in ['ACTION_VOTE', 'ACTION_DELEGATE', 'ACTION_EVM', 'ACTION_IBC_TRANSFER']:
            actions.append(Claim(action=action, completed=False, claimable_amount='0'))
        return (ClaimsData(initial_claimable_amount='0', claims=actions))

    elif r.status_code == 400:
        return ClaimsResponse(error='invalid wallet')

    raise HTTPException(
        status_code=r.status_code,
        detail=r.reason,
    )
