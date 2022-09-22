from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import CharityBase


class Donation(CharityBase):
    '''Модель пожертвований'''
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
