from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.services.investment import close_investment


async def check_charity_project_exists(
    project_id: int, session: AsyncSession
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(status_code=404, detail='Проект не найден!')
    return project


async def check_name_duplicate(
    project_name: str, session: AsyncSession
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400, detail='Проект с таким именем уже существует!',
        )


def check_project_fully_invested(project: CharityProject) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=400, detail='Закрытый проект нельзя редактировать!'
        )


def check_project_is_invested(project: CharityProject) -> None:
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


def check_full_amount(
    project: CharityProject, full_amount: int
) -> CharityProject:
    if full_amount < project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail='В проект уже было внесено больше средств!'
        )
    if full_amount == project.invested_amount:
        close_investment(project)
    return project
