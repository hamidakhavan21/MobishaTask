import httpx
from app.persist.token_repository import TokenRepository
from app.config.settings import DIGIKALA_API_BASE_URL

class AuthService:
    def __init__(self, token_repo: TokenRepository):
        self.token_repo = token_repo

    async def send_otp(self, username: str):
        otp_url = f"{DIGIKALA_API_BASE_URL}/otp/send"
        payload = {"username": username}
        async with httpx.AsyncClient() as client:
            response = await client.post(otp_url, json=payload)
        return response

    async def verify_otp(self, username: str, otp: str):
        otp_url = f"{DIGIKALA_API_BASE_URL}/otp/verify"
        payload = {"otp": otp, "username": username}
        async with httpx.AsyncClient() as client:
            response = await client.post(otp_url, json=payload)
        if response.status_code == 201:
            response_data = response.json()
            token = response_data.get("data", {}).get("token", {}).get("access_token")
            if token:
                await self.token_repo.save_token(
                    username=username,
                    access_token=token,
                    refresh_token=response_data["data"]["token"]["refresh_token"],
                    expire_in=response_data["data"]["token"]["expire_in"],
                )
            return response
        return response

