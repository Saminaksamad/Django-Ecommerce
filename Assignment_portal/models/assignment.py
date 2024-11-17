from pymongo import MongoClient
from config import MONGO_URI

# Create a MongoDB client connection
client = MongoClient(MONGO_URI)

# Get the default database from the connection
db = client.get_database()

class Assignment:
    """
    A utility class to interact with the 'assignments' collection in the MongoDB database.
    Provides methods to query, insert, and update assignment documents.
    """

    @staticmethod
    def collection():
        """
        Returns the 'assignments' collection from the database.
        This is the main collection where assignment documents are stored.
        """
        return db.assignments

    @staticmethod
    def find(query):
        """
        Finds all documents in the 'assignments' collection that match the given query.
        
        Args:
            query (dict): The query filter to match documents in the collection.
        
        Returns:
            list: A list of matching documents.
        """
        return list(Assignment.collection().find(query))

    @staticmethod
    def insert_one(data):
        """
        Inserts a single document into the 'assignments' collection.
        
        Args:
            data (dict): The data to insert as a document into the collection.
        
        Returns:
            pymongo.results.InsertOneResult: The result of the insert operation.
        """
        return Assignment.collection().insert_one(data)

    @staticmethod
    def update_one(query, update):
        """
        Updates a single document in the 'assignments' collection that matches the given query.
        
        Args:
            query (dict): The query filter to match the document to update.
            update (dict): The update operations to apply to the matched document.
        
        Returns:
            pymongo.results.UpdateResult: The result of the update operation.
        """
        return Assignment.collection().update_one(query, update)
