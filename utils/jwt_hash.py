from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def _hash(password: str) -> str:
    return pwd_context.hash(password)


def verify(plain_password: str, hash_password: str) -> bool:
    return pwd_context.verify(plain_password, hash_password)
