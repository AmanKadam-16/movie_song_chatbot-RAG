from fastapi import APIRouter, HTTPException, Depends, status
from movie_assistant.schemas import user as user_schema
from movie_assistant.services import auth as auth_service
from movie_assistant.utils.auth import create_token, get_current_user
from sqlalchemy.orm import Session
from movie_assistant.database.deps import get_db


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=user_schema.UserBase)
def register(user_info: user_schema.AddUser, db: Session = Depends(get_db)):
    try:
        service_response = auth_service.register_user(user_info=user_info, db=db)
        return service_response
    except HTTPException as he:
        raise HTTPException(
            status_code=he.status_code, detail=f"HTTP Error : {he.detail}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server Error : {e}",
        )


@router.post("/login", response_model=user_schema.LoginResponse)
def login_user(user_credentials: user_schema.GetUser, db: Session = Depends(get_db)):
    try:
        service_response = auth_service.get_user_info(
            user_credentials=user_credentials, db=db
        )
        data = {}
        data["sub"] = str(service_response.id)
        data["role"] = service_response.role
        access_token = create_token(data=data)
        login_response = user_schema.LoginResponse(
            first_name=service_response.first_name,
            last_name=service_response.last_name,
            email=service_response.email,
            token=access_token,
        )

        return login_response
    except HTTPException as he:
        raise HTTPException(
            status_code=he.status_code, detail=f"HTTP Error : {he.detail}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server Error : {e}",
        )


@router.get("/me")
def check(user=Depends(get_current_user)):
    return "hello world"
