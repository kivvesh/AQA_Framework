from pydantic import BaseModel,Field



class ResponseDataUser(BaseModel):
    """Модель ответа по пользователю"""
    id:int = Field(title='id')
    email:str = Field(title='email')
    first_name:str = Field(title='first_name')
    last_name:str = Field(title='last_name')
    avatar:str = Field(title='avatar')
