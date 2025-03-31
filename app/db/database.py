import motor.motor_asyncio
from app.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
database = client[settings.DATABASE_NAME]

users_collection = database.users
books_collection = database.books