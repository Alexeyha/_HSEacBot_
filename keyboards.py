from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import utils
import random


def greet_after_start():
    button_add_base = KeyboardButton('/Пополнить базу студентов')
    button_memorize = KeyboardButton('/Начать запоминание')
    greet = ReplyKeyboardMarkup(resize_keyboard=True)
    greet.add(button_memorize).add(button_add_base)
    return greet


def create_greet(chat_id, answer, sex):
    variants = utils.get_variants(chat_id, answer, sex)
    random.shuffle(variants)
    greet = ReplyKeyboardMarkup()
    button_1 = KeyboardButton(variants[0])
    button_2 = KeyboardButton(variants[1])
    greet.row(button_1, button_2)
    button_3 = KeyboardButton(variants[2])
    button_4 = KeyboardButton(variants[3])
    greet.row(button_3, button_4)
    button_5 = KeyboardButton("/Отмена")
    greet.add(button_5)
    return greet


def greet_cancel():
    greet = ReplyKeyboardMarkup(resize_keyboard=True)
    button_cancel = KeyboardButton("/Отмена")
    greet.add(button_cancel)
    return greet


def greet_course():
    greet = ReplyKeyboardMarkup()
    button_1 = KeyboardButton("1")
    button_2 = KeyboardButton("2")
    greet.row(button_1, button_2)
    button_3 = KeyboardButton("3")
    button_4 = KeyboardButton("4")
    greet.row(button_3, button_4)
    button_5 = KeyboardButton("/Отмена")
    greet.add(button_5)
    return greet


def greet_memorize_course():
    greet = ReplyKeyboardMarkup()
    button_0 = KeyboardButton("Все")
    button_1 = KeyboardButton("1")
    button_2 = KeyboardButton("2")
    greet.row(button_1, button_2)
    button_3 = KeyboardButton("3")
    button_4 = KeyboardButton("4")
    greet.row(button_3, button_4)
    greet.add(button_0)
    return greet


def greet_test_photo():
    greet = ReplyKeyboardMarkup()
    button_0 = KeyboardButton("Да")
    greet.add(button_0)
    button_1 = KeyboardButton("Нет")
    greet.add(button_1)
    return greet
