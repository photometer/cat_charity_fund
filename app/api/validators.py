from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.services.investment import close_investment


async def check_charity_project_exists(
    project_id: int, session: AsyncSession
) -> CharityProject:
    """Check the project availability by id."""
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(status_code=404, detail='Project was not found!')
    return project


async def check_name_duplicate(
    project_name: str, session: AsyncSession
) -> None:
    """Check the uniqueness of the project name."""
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Project with the same name already exists!',
        )


def check_project_fully_invested(project: CharityProject) -> None:
    """Check if project is closed."""
    if project.fully_invested:
        raise HTTPException(
            status_code=400, detail='Closed project cannot be edited!'
        )


def check_project_is_invested(project: CharityProject) -> None:
    """Check if funds are invested in the project."""
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='Funds have been contributed to the project, cannot be deleted!'
        )


def check_full_amount(
    project: CharityProject, full_amount: int
) -> CharityProject:
    """Validate full_amount field changes."""
    if full_amount < project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail='More funds have already been contributed to the project!'
        )
    if full_amount == project.invested_amount:
        close_investment(project)
    return project
