from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from app.db.init_db import get_db_connection
from app.models.user import UserLoginRequest, LoginResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
def login(payload: UserLoginRequest):
    """
    Users can log in via the Login Screen.
    Authenticates student or faculty user against the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, email, role, password_hash FROM users WHERE email = ?",
        (payload.email.lower(),)
    )
    user = cursor.fetchone()
    conn.close()

    if not user or user["password_hash"] != payload.password:
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = f"jwt-token-mock-{user['id']}"
    return LoginResponse(
        token=token,
        user=UserResponse(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            role=user["role"]
        )
    )


@router.get("/me", response_model=UserResponse)
def get_current_user(authorization: Optional[str] = Header(None)):
    """Returns current user profile."""
    # Default to Alex Morgan if no header provided
    user_id = "usr_alex_001"
    if authorization and "usr_" in authorization:
        for part in authorization.split("-"):
            if part.startswith("usr_"):
                user_id = part
                break

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, role FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return UserResponse(
            id="usr_alex_001",
            name="Alex Morgan",
            email="alex@smartstudy.edu",
            role="student"
        )

    return UserResponse(
        id=user["id"],
        name=user["name"],
        email=user["email"],
        role=user["role"]
    )
