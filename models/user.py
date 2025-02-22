import datetime

from pydantic import BaseModel,Field


class ResponseDataUser(BaseModel):
    """Модель ответа по пользователю"""
    id:int = Field(title='id')
    email:str = Field(title='email')
    first_name:str = Field(title='first_name')
    last_name:str = Field(title='last_name')
    avatar:str = Field(title='avatar')

class ResponsePostUser(BaseModel):
    """Модель ответа по созданию пользователя"""
    name:str = Field(title='name')
    job:str = Field(title='job')
    id:str = Field(title='id')
    createdAt:datetime.datetime = Field(title='createdAt')