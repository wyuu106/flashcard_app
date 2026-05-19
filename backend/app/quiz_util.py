import random

# 選択肢を作る関数
def create_choices(correct_meaning, all_meanings):
    others = [m for m in all_meanings if m != correct_meaning]

    choices = [correct_meaning] + random.sample(others, 3)

    random.shuffle(choices)

    return choices