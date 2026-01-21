# test_delete_account.py

from models.account_service import AccountService

USER_ID = "6970b4f176b3c2e4f7c3f467"

deleted = AccountService.delete_account(USER_ID)
print("Account deleted:", deleted)
