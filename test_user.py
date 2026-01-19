from models.user_model import UserModel

user = UserModel.create_user("player1", "password")
print("Created:", user)

user = UserModel.authenticate("player1", "password")
print("Authenticated:", user)
