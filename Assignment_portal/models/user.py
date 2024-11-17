from pymongo import MongoClient
from config import MONGO_URI

# Create a MongoDB client connection
client = MongoClient(MONGO_URI)

# Get the default database from the connection
db = client.get_database()

class User:
    """
    A utility class to interact with the 'users' collection in the MongoDB database.
    Provides methods to query and insert user documents.
    """

    @staticmethod
    def collection():
        """
        Returns the 'users' collection from the database.
        This is the main collection where user-related documents are stored.
        
        Returns:
            pymongo.collection.Collection: The MongoDB collection object for 'users'.
        """
        return db.users

    @staticmethod
    def find_one(query):
        """
        Finds a single document in the 'users' collection that matches the given query.
        
        Args:
            query (dict): The query filter to match a document in the collection.
        
        Returns:
            dict or None: The first matching document, or None if no document matches.
        """
        return User.collection().find_one(query)

    @staticmethod
    def insert_one(data):
        """
        Inserts a single document into the 'users' collection.
        
        Args:
            data (dict): The data to insert as a document into the collection.
        
        Returns:
            pymongo.results.InsertOneResult: The result of the insert operation.
        """
        return User.collection().insert_one(data)
