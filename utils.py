from database import df_names, df_popular_names
import random


def check_name(name):
    if df_names[df_names['Name'] == name].empty:
        return False

    if df_names[df_names['Name'] == name]['Sex'].values == 'Ж':
        return 'female'
    return 'male'


def get_variants(chat_id, answer, sex):
    variants = [answer]
    if sex == 'male':
        sex = 'М'
        max_number = 385
        min_number = 196
    else:
        sex = 'Ж'
        max_number = 196
        min_number = 0
    while len(variants) != 4:
        number = random.randrange(min_number, max_number)
        var = df_popular_names[df_popular_names['Sex'] == sex]['Names'][number]
        if var not in variants:
            variants.append(var)
    return variants




