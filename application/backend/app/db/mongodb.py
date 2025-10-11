"""
MongoDB connection and database management
"""
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class MongoDB:
    """MongoDB connection manager"""
    
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None
    
    @classmethod
    async def connect_db(cls):
        """Connect to MongoDB"""
        try:
            logger.info("Connecting to MongoDB...")
            cls.client = AsyncIOMotorClient(
                settings.MONGO_URL,
                maxPoolSize=settings.MONGO_MAX_POOL_SIZE,
                minPoolSize=settings.MONGO_MIN_POOL_SIZE,
            )
            cls.db = cls.client[settings.MONGO_DB_NAME]
            
            # Test connection
            await cls.client.admin.command('ping')
            logger.info(f"Successfully connected to MongoDB database: {settings.MONGO_DB_NAME}")
            
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise
    
    @classmethod
    async def close_db(cls):
        """Close MongoDB connection"""
        if cls.client:
            logger.info("Closing MongoDB connection...")
            cls.client.close()
            logger.info("MongoDB connection closed")
    
    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        """Get database instance"""
        if cls.db is None:
            raise Exception("Database not initialized. Call connect_db() first.")
        return cls.db
    
    @classmethod
    def get_collection(cls, collection_name: str):
        """Get collection by name"""
        db = cls.get_db()
        return db[collection_name]


# Database dependency for FastAPI
async def get_database() -> AsyncIOMotorDatabase:
    """Dependency to get database instance"""
    return MongoDB.get_db()

