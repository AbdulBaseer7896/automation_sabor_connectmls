# from db import mongo

# def insert_user(data):
#     return mongo.db.users.insert_one(data)

# def get_all_users():
#     return list(mongo.db.users.find({}, {"_id": 0}))

# def delete_user(email):
#     return mongo.db.users.delete_one({"email": email})

# def update_user(email, new_data):
#     return mongo.db.users.update_one({"email": email}, {"$set": new_data})




from db import mongo

def save_json(data, collection_name="default_collection"):
    """
    Save JSON data into MongoDB.
    
    Args:
        data (dict): JSON data to insert
        collection_name (str): MongoDB collection name (default: 'default_collection')
    
    Returns:
        Inserted document ID
    """
    print("this is hte saving json funciton = " , data)
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary (JSON).")
    print("this is hte saving json funciton 2 = " )
    collection = mongo.db[collection_name]
    print("this is hte saving json funciton 3 = " )
    result = collection.insert_one(data)
    print("this is hte saving json funciton 4 = " )
    return str(result.inserted_id)


def get_all_json(collection_name="default_collection"):
    """
    Get all documents from the given collection (without _id).
    """
    collection = mongo.db[collection_name]
    return list(collection.find({}, {"_id": 0}))


def delete_json(filter_query, collection_name="default_collection"):
    """
    Delete a document from the collection by filter.
    Example filter_query = {"status": "error"}
    """
    collection = mongo.db[collection_name]
    return collection.delete_one(filter_query)


def update_json(filter_query, new_data, collection_name="default_collection"):
    """
    Update a document in the collection by filter.
    Example filter_query = {"status": "error"}
    Example new_data = {"status": "success"}
    """
    collection = mongo.db[collection_name]
    return collection.update_one(filter_query, {"$set": new_data})
