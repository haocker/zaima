from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from ..schemas.contact import ContactCreate, ContactUpdate, ContactResponse
from ..services.contact import (
    get_user_contact,
    create_or_update_contact,
    update_contact_partial,
    delete_contact
)
from ..utils.database import get_db
from ..api.deps import get_current_user
from ..models.user import User

router = APIRouter()


@router.post("/", response_model=ContactResponse, summary="创建或更新紧急联系人")
def create_or_update_user_contact(
    contact_data: ContactCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    创建或更新用户的紧急联系人：
    - 如果用户已有联系人，更新现有联系人
    - 如果用户没有联系人，创建新联系人
    """
    contact = create_or_update_contact(db, current_user, contact_data)
    return ContactResponse.model_validate(contact)


@router.get("/", response_model=Optional[ContactResponse], summary="获取紧急联系人")
def get_contact(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户的紧急联系人信息
    """
    contact = get_user_contact(db, current_user)
    if not contact:
        return None
    return ContactResponse.model_validate(contact)


@router.patch("/", response_model=ContactResponse, summary="部分更新紧急联系人")
def update_contact(
    contact_update: ContactUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    部分更新用户的紧急联系人信息
    """
    contact = update_contact_partial(db, current_user, contact_update)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未找到紧急联系人信息"
        )
    return ContactResponse.model_validate(contact)


@router.delete("/", summary="删除紧急联系人")
def remove_contact(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    删除用户的紧急联系人
    """
    success = delete_contact(db, current_user)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未找到紧急联系人信息"
        )
    return {"message": "紧急联系人已删除"}