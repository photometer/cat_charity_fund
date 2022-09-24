from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import CharityBase


class Donation(CharityBase):
    """Модель пожертвований."""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return (
            f'№{self.id}. Вложено: {self.invested_amount}/{self.full_amount}'
        )
