from fastapi import APIRouter, HTTPException
from app.models.requests import SendOTPRequest, VerifyOTPRequest
from app.persist.token_repository import TokenRepository
from app.services.auth_service import AuthService
from app.config.settings import MONGO_URI, DB_NAME
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
token_repo = TokenRepository(db)
auth_service = AuthService(token_repo)

router = APIRouter()

@router.post("/send-otp")
async def send_otp(data: SendOTPRequest):
    response = await auth_service.send_otp(data.username)
    if response.status_code == 200:
        return {"message": "OTP sent successfully"}
    raise HTTPException(status_code=response.status_code, detail="Failed to send OTP")

@router.post("/verify-otp")
async def verify_otp(data: VerifyOTPRequest):
    response = await auth_service.verify_otp(data.username, data.otp)
    if response.status_code == 201:
        return {"message": "Token verified and stored successfully"}
    raise HTTPException(status_code=response.status_code, detail="Failed to verify OTP")
