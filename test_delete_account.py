# test_delete_account.py

from models.account_service import AccountService

USER_ID = "697e5fdfb5a29b3d40ec4662"

deleted = AccountService.delete_account(USER_ID)
print("Account deleted:", deleted)
