from motor.motor_asyncio import AsyncIOMotorDatabase

class TokenRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["tokens"]

    async def save_token(self, username: str, access_token: str, refresh_token: str, expire_in: int):
        await self.collection.update_one(
            {"username": username},
            {
                "$set": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "expire_in": expire_in,
                }
            },
            upsert=True,
        )

    async def get_token(username: str, db: AsyncIOMotorDatabase):
        token = await db.tokens.find_one({"username": username})
        if not token:
            raise ValueError("Token not found for the specified username")
        return token

