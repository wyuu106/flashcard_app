from app.models.user_model import User

MAX_LEVEL = 100

def required_exp(level):
    if level < 60:
        return level * 100
    
    if 60 <= level:
        return 2 ** (level // 6)

def level_up(user: User, get_exp: int) -> User:
    level = user.level
    exp = user.exp + get_exp

    while level <= MAX_LEVEL:
        need = required_exp(level)

        if exp < need:
            break

        exp -= need
        level += 1

        if level == 100:
            exp = 0

    user.level = level
    user.exp = exp

    return user