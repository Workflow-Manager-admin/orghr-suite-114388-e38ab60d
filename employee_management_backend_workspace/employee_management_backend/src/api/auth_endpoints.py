from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .models import Token, UserLogin, Employee
from .auth import authenticate_user, create_access_token, get_current_active_user
from datetime import timedelta

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

# PUBLIC_INTERFACE
@router.post("/login", response_model=Token, summary="Authenticate and get JWT token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a user and returns a JWT access token.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

# PUBLIC_INTERFACE
@router.get("/me", response_model=Employee, summary="Get current user")
async def get_me(current_user: Employee = Depends(get_current_active_user)):
    """
    Get current authenticated user details.
    """
    return current_user

# PUBLIC_INTERFACE
@router.post("/logout", summary="Logout (client side)")
async def logout():
    """
    Dummy logout endpoint. JWT-based logout is client-side only (stateless).
    Invalidate token on client (Front-End should remove token).
    """
    return {"message": "Logged out"}
