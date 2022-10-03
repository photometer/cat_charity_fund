from datetime import datetime
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.crud.base import CRUDBase

ModelType = TypeVar('ModelType', bound=Base)
CRUDType = TypeVar('CRUDType', bound=CRUDBase)


def close_investment(obj: ModelType) -> None:
    """Setting attributes for a closed project/donation."""
    obj.fully_invested = True
    obj.close_date = datetime.now()


async def investment(
    invest_from: ModelType, invest_in: CRUDType, session: AsyncSession
) -> ModelType:
    """
    Distributing donations process when creating a new project/donation.
    """
    objects = await invest_in.get_multi_open(session)
    for object in objects:
        for_invest = invest_from.full_amount - invest_from.invested_amount
        investitions = object.full_amount - object.invested_amount
        to_invest = min(for_invest, investitions)
        object.invested_amount += to_invest
        invest_from.invested_amount += to_invest
        if object.full_amount == object.invested_amount:
            close_investment(object)
        if invest_from.full_amount == invest_from.invested_amount:
            close_investment(invest_from)
            break
    session.add_all((*objects, invest_from))
    await session.commit()
    await session.refresh(invest_from)
    return invest_from
