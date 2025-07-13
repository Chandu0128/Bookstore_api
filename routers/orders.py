from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
import models, schemas
from database import get_db
from auth import get_current_user
from typing import List

# Define OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# Create a new order (requires authentication)
@router.post("/", response_model=schemas.OrderOut)
def place_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    book = db.query(models.Book).filter(models.Book.id == order.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.stock < order.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    book.stock -= order.quantity  # reduce stock

    new_order = models.Order(
        user_id=current_user.id,
        book_id=order.book_id,
        quantity=order.quantity
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order

# Get all orders placed by the currently authenticated user
@router.get("/myorders", response_model=List[schemas.OrderOut])
def get_user_orders(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Order).filter(models.Order.user_id == current_user.id).all()

# Admin-style route: Get all orders (any user) - requires token
@router.get("/", response_model=List[schemas.OrderOut])
def get_all_orders(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    return db.query(models.Order).all()
