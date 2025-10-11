"""
MongoDB operations service
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.db.mongodb import MongoDB
from app.core.logging import get_logger

logger = get_logger(__name__)


class MongoService:
    """MongoDB operations service"""
    
    def __init__(self):
        self.db_name = "stylic"
    
    def get_db(self) -> AsyncIOMotorDatabase:
        """Get database instance"""
        return MongoDB.get_db()
    
    def get_collection(self, collection_name: str):
        """Get collection by name"""
        return MongoDB.get_collection(collection_name)
    
    async def insert_one(
        self,
        collection_name: str,
        document: Dict[str, Any]
    ) -> Optional[str]:
        """
        Insert a single document
        
        Args:
            collection_name: Name of the collection
            document: Document to insert
            
        Returns:
            Inserted document ID or None
        """
        try:
            collection = self.get_collection(collection_name)
            result = await collection.insert_one(document)
            logger.info(f"Inserted document in {collection_name}: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error inserting document in {collection_name}: {str(e)}")
            return None
    
    async def find_one(
        self,
        collection_name: str,
        query: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Find a single document
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            
        Returns:
            Found document or None
        """
        try:
            collection = self.get_collection(collection_name)
            document = await collection.find_one(query)
            return document
        except Exception as e:
            logger.error(f"Error finding document in {collection_name}: {str(e)}")
            return None
    
    async def find_many(
        self,
        collection_name: str,
        query: Dict[str, Any],
        sort: Optional[List[tuple]] = None,
        limit: Optional[int] = None,
        skip: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Find multiple documents
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            sort: Sort specification
            limit: Maximum number of documents to return
            skip: Number of documents to skip
            
        Returns:
            List of found documents
        """
        try:
            collection = self.get_collection(collection_name)
            cursor = collection.find(query)
            
            if sort:
                cursor = cursor.sort(sort)
            if skip:
                cursor = cursor.skip(skip)
            if limit:
                cursor = cursor.limit(limit)
            
            documents = await cursor.to_list(length=limit if limit else None)
            return documents
        except Exception as e:
            logger.error(f"Error finding documents in {collection_name}: {str(e)}")
            return []
    
    async def update_one(
        self,
        collection_name: str,
        query: Dict[str, Any],
        update: Dict[str, Any],
        upsert: bool = False
    ) -> bool:
        """
        Update a single document
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            update: Update operations
            upsert: Whether to insert if not found
            
        Returns:
            True if successful, False otherwise
        """
        try:
            collection = self.get_collection(collection_name)
            
            # Add updated_at timestamp
            if "$set" not in update:
                update["$set"] = {}
            update["$set"]["updated_at"] = datetime.utcnow()
            
            result = await collection.update_one(query, update, upsert=upsert)
            logger.info(f"Updated document in {collection_name}: matched={result.matched_count}, modified={result.modified_count}")
            return result.modified_count > 0 or result.upserted_id is not None
        except Exception as e:
            logger.error(f"Error updating document in {collection_name}: {str(e)}")
            return False
    
    async def update_many(
        self,
        collection_name: str,
        query: Dict[str, Any],
        update: Dict[str, Any]
    ) -> int:
        """
        Update multiple documents
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            update: Update operations
            
        Returns:
            Number of documents modified
        """
        try:
            collection = self.get_collection(collection_name)
            
            # Add updated_at timestamp
            if "$set" not in update:
                update["$set"] = {}
            update["$set"]["updated_at"] = datetime.utcnow()
            
            result = await collection.update_many(query, update)
            logger.info(f"Updated documents in {collection_name}: matched={result.matched_count}, modified={result.modified_count}")
            return result.modified_count
        except Exception as e:
            logger.error(f"Error updating documents in {collection_name}: {str(e)}")
            return 0
    
    async def delete_one(
        self,
        collection_name: str,
        query: Dict[str, Any]
    ) -> bool:
        """
        Delete a single document
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            
        Returns:
            True if successful, False otherwise
        """
        try:
            collection = self.get_collection(collection_name)
            result = await collection.delete_one(query)
            logger.info(f"Deleted document in {collection_name}: deleted={result.deleted_count}")
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting document in {collection_name}: {str(e)}")
            return False
    
    async def count_documents(
        self,
        collection_name: str,
        query: Dict[str, Any]
    ) -> int:
        """
        Count documents matching query
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            
        Returns:
            Number of matching documents
        """
        try:
            collection = self.get_collection(collection_name)
            count = await collection.count_documents(query)
            return count
        except Exception as e:
            logger.error(f"Error counting documents in {collection_name}: {str(e)}")
            return 0
    
    async def distinct(
        self,
        collection_name: str,
        field: str,
        query: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """
        Get distinct values for a field
        
        Args:
            collection_name: Name of the collection
            field: Field name
            query: Optional query filter
            
        Returns:
            List of distinct values
        """
        try:
            collection = self.get_collection(collection_name)
            values = await collection.distinct(field, query or {})
            return values
        except Exception as e:
            logger.error(f"Error getting distinct values in {collection_name}: {str(e)}")
            return []


# Create global mongo service instance
mongo_service = MongoService()

