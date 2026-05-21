from app.models.user_model import User

MAX_LEVEL = 100

def required_exp(level):
    if level < 20:
        return level * 30
    
    elif 20 <= level < 40:
        return level * 50
    
    elif 40 <= level < 60:
        return level * 100

    elif 60 <= level < 80:
        return level * 150

    elif 80 <= level < 90:
        return level * 200
    
    elif 90 <= level < 95:
        return level * 300
    
    elif 95 <= level < 99:
        return level * 500

def level_up(user: User, get_exp: int) -> User:
    level = user.level
    exp = user.exp + get_exp

    while level <= MAX_LEVEL:
        need = required_exp(level) # level upに必要なexp

        if exp < need:
            break

        exp -= need
        level += 1

        if level == MAX_LEVEL:
            exp = 0

    user.level = level
    user.exp = exp

    return user