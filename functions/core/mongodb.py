from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId

class MGConection:
    def __init__(self, db_name):
        self.password = "vpi167trungkinh"
        self.db_name = db_name
        self.client = MongoClient(f"mongodb+srv://tuananguyenvpi:{self.password}@vpi167trungkinh.sog7blp.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client[db_name]

    def get_list_databases(self):
        return list(self.client.list_database_names())

    def delete_database(self, db_name):
        try:
            self.client.drop_database(db_name)
            print(f"Deleted database {db_name}")
        except Exception as e:
            print(e)
    def create_database(self, db_name):
        self.client[db_name]
        print(f"Created database {db_name}")
    
    def get_list_collections(self):
        return self.db.list_collection_names()
    
    def delete_collection(self, collection_name):
        try:
            self.db.drop_collection(collection_name)
            print(f"Deleted collection {collection_name}")
        except Exception as e:
            print(e)
        
    def create_collection(self, collection_name):
        try:
            self.db.create_collection(collection_name)
            print(f"Created collection {collection_name}")
        except Exception as e:
            print(e)

class MGCollection(MGConection):
    def __init__(self, db_name, collection_name):
        super().__init__(db_name)
        self.collection_name = collection_name
        self.collection = self.db[self.collection_name]
        self.collection.drop_indexes()
        self.collection.create_index(
            {
                "Name": "text",
            }
        )

    def insert_one(self, data):
        try:
            self.collection.insert_one(data)
            print(f"Inserted one document to collection {self.collection_name}")
        except Exception as e:
            print(e)

    def insert_many(self, data):
        try:
            self.collection.insert_many(data)
            print(f"Inserted many documents to collection {self.collection_name}")
        except Exception as e:
            print(e)

    def get_all_docs(self, limit=None):
        if limit is None:
            return self.collection.find()
        else:
            return self.collection.find().limit(limit)

    def get_doc_keys(self):
        return list(self.collection.find_one().keys())
    
    def get_unique_values(self, key, filter={}):
        return list(self.collection.distinct(key, filter))

    def delete_doc_by_id(self, id):
        try:
            self.collection.delete_one({"_id": ObjectId(id)})
            print(f"Deleted document with id {id}")
        except Exception as e:
            print(e)

    # Get docs by key, value
    def get_docs_by_key_value(self, key, value):
        return self.collection.find({key: value})
    
    # Get docs by multiple keys, values
    def get_docs_by_multiple_key_values(self, key_values):
        return self.collection.find(key_values)
    
    # Count, Sort, Limit when finding docs
    def keyword_search(self, text: str):
        return self.collection.find(
            { '$text':
                { 
                    '$search': text,
                },
                
            }
        )

