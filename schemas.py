from pydantic import BaseModel, EmailStr
from typing import List

# -------------------- USER SCHEMAS --------------------

class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


# -------------------- BOOK SCHEMAS --------------------

class BookBase(BaseModel):
    title: str
    author: str
    category: str
    price: float
    stock: int


class BookCreate(BookBase):
    pass


class BookOut(BookBase):
    id: int

    class Config:
        from_attributes = True


# -------------------- ORDER SCHEMAS --------------------

class OrderCreate(BaseModel):
    book_id: int
    quantity: int


# This will return full order info with nested User and Book
class OrderOut(BaseModel):
    id: int
    quantity: int
    user: UserOut
    book: BookOut

    class Config:
        from_attributes = True
