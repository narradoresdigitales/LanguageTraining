# models/account_service.py

from models.user_model import UserModel
from models.progress_model import ProgressModel

class AccountService:
    @staticmethod
    def delete_account(user_id: str) -> bool:
        """
        Delete a user account and all associated data.
        Returns True if user was deleted.
        """
        progress_deleted = ProgressModel.delete_progress(user_id)
        user_deleted = UserModel.delete_user(user_id)

        return user_deleted
