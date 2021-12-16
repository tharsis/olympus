from typing import List

from evmosgrpc.accounts import get_account_all_balances
from fastapi import APIRouter
from fastapi import Depends
from pydantic.main import BaseModel
from sqlalchemy.orm import Session
from src.database import session_for_request
from src.endpoints.constants import BLOCKCHAIN_TAG

router = APIRouter()


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
