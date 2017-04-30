"""
All data must be only manipulated through this middleware,
and not directly using Pymongo.
"""

from .mongo import DB


class DAO(object):
    """
    Implements a generic middleware for accessing DB.

    Note that this instance itself don't represent anything at domain,
    it's just useful for accessing dictionaries that stands for documents
    from a certain database collection.
    """


    def __init__(self, collection: str):
        """
        Don't use this constructor directly as you're probably doing now.
        Use a factory instead!

        Create an instance for starting using data access methods.

        All data access will assume as context the given collection.

        TODO: check if the collection exists and raise a custom exception if it doesn't
        """
        self.collection = collection



    def find_all(self):
        """
        Gets a list of all the documents from the collection.
        TODO: retrieve only logical alive documents (maybe a 'alive_only=True' param?)
        """
        return DB[self.collection].find_all()



    def find_one(self, conditions: dict):
        """
        Gets a single found document with the given conditions, returns it as dict.
        TODO: retrieve only logical alive documents (maybe a 'alive_only=True' param?)
        """
        return DB[self.collection].find_one(conditions)



    def find(self, conditions: dict):
        """
        Filters documents from database collection. The given dictionary param
        represents the filter json. Returns a list of dicts, where each of them
        is a found document.
        TODO: retrieve only logical alive documents (maybe a 'alive_only=True' param?)
        """
        return DB[self.collection].find(conditions)



    def insert_one(self, document: dict):
        """
        Insert a document as dict into the collection and returns its new id if it worked.
        TODO: insert an alive document
        """
        return DB[self.collection].insert_one(document).inserted_id



    def insert_many(self, document: list):
        """
        TODO: Insert a list of documents into the collection and returns a list of their
        new ids if it worked.
        """
        raise NotImplementedError("Tried to call an update function without implementing it.")



    def update(self, document: dict):
        """
        TODO: implement an update for a single document.
        """
        raise NotImplementedError("Tried to call an update function without implementing it.")



    def delete(self, document: dict):
        """
        TODO: Logical delete. So the document still recorded at persistence,
        but can no longer be retrieved using regular CRUD methods.
        """
        raise NotImplementedError("Need to implement update function for logical deleting it.")