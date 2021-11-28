import pandas as pd
import uuid
import os

df = pd.read_csv('data.csv')

df_names = pd.read_csv('names.csv')

df_popular_names = pd.read_csv('popular.csv')


def get_photo(course):
    if course == 0:
        part_df = df.sample()
        photo_id = part_df["photo_id"].values[0]
        name_student = part_df["name_student"].values[0].split()[1]
        sex = part_df["sex"].values[0]
        return [photo_id, name_student, sex]

    part_df = df[df['course'] == course].sample()
    photo_id = part_df["photo_id"].values[0]
    name_student = part_df["name_student"].values[0].split()[1]
    sex = part_df["sex"].values[0]
    return [photo_id, name_student, sex]


def add_photo(name_student, course, sex, file):
    global df
    unique_filename = 'photos/' + str(uuid.uuid4()) + '.jpg'
    os.rename(file, unique_filename)
    df_new = pd.DataFrame(
        {'photo_id': [unique_filename], 'name_student': [name_student], 'course': [int(course)], 'sex': sex})
    df_new.to_csv('data.csv', mode="a", index=False, header=False)
    df = df.append(df_new, ignore_index=True)


def check_empty_course(course):
    if course == 0:
        if df.empty:
            return True
    elif df[df['course'] == course].empty:
        return True
    return False
