import bcrypt

async def hash_password(plain_password: str) -> tuple[str, str]:
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return salt.decode(), hashed.decode()

async def verify_password(plain_password: str, salt: str, password_hash: str) -> bool:
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt.encode())
    return hashed.decode() == password_hash
