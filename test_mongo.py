from models.user_model import db

if db:
    print("MongoDB connected!")
    print("Collections:", db.list_collection_names())
else:
    print("No DB connection.")
