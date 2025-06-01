from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserLogin, UserRead, Token, UserCreate
from app.models.users import User
from app.core.security import hash_password
from app.db.session import get_async_session
from sqlalchemy.future import select
from app.core.security import verify_password, create_access_token
import uuid
import random

router = APIRouter()


@router.post("/", response_model=UserRead, summary='Register a new user')
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(User).filter(User.email == user_in.email))
    user = result.scalar_one_or_none()
    if user:
        raise HTTPException(status_code=400, detail='Email already registered')

    verification_code = str(random.randint(100000, 999999))
    print(f"Verification code for {user_in.email}: {verification_code}")

    new_user = User(
        id=str(uuid.uuid4()),
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        is_active=True,
        is_verified=False,
        verification_code=verification_code,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/verify", summary="Verify a user by code")
async def verify_user(code: str, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(User).filter(User.verification_code == code))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid verification code")

    user.is_verified = True
    user.is_active = True
    user.verification_code = None

    db.add(user)
    await db.commit()
    return {"message": "User successfully verified"}



@router.post("/login", response_model=Token)
async def login(user_login: UserLogin, session: AsyncSession = Depends(get_async_session)):
    stmt = select(User).where(User.email == user_login.email)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}