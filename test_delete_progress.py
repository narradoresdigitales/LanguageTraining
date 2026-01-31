from models.progress_model import ProgressModel

USER_ID = "Antonio"  # change to an existing user

print("Before delete:")
print(ProgressModel.load_progress(USER_ID))

deleted = ProgressModel.delete_progress(USER_ID)
print("Deleted:", deleted)

print("After delete:")
print(ProgressModel.load_progress(USER_ID))
