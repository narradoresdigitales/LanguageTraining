from hashlib import sha256

password = "password"
pw_hash = sha256(password.encode()).hexdigest()
print(pw_hash)
