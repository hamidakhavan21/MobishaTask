from pydantic import BaseModel

class SendOTPRequest(BaseModel):
    username: str

class VerifyOTPRequest(BaseModel):
    username: str
    otp: str
class ProductResponse(BaseModel):
    product_id: str
    dkpc: str
    name: str
    price: float
    stock: int
    isActive: bool   
