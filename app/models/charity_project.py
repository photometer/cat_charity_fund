from sqlalchemy import Column, String, Text

from .base import CharityBase


class CharityProject(CharityBase):
    """Charity projects model."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'{self.name}. Collected {self.invested_amount}/{self.full_amount}'
        )
