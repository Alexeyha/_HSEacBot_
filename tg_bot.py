from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.message import ContentType
from aiogram.dispatcher import FSMContext

from config import TOKEN
import utils
import keyboards
import statements as stm
import database as db
from photo_proc import imaginate

API_TOKEN = TOKEN

bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def run_command(chat_id):
    await bot.send_message(chat_id, text="Выберите, что вы хочешь.",
                           reply_markup=keyboards.greet_after_start())


@dp.message_handler(commands=['start'])
async def run_command_start(message: types.Message):
    await message.answer('Привет!\nЯ бот, помогающий запомнить людей с твоего факультета.\n'
                         'Выберите, что вы хотите сделать.',
                         reply_markup=keyboards.greet_after_start())


@dp.message_handler(commands=['help'])
async def run_command_help(message: types.Message):
    await message.reply('Мои команды:\nНачать запоминание - выберите курс, студентов которого '
                        'вы хотите запомнить и старайтесь угадывать правильное имя человека по его фото.\n'
                        'Пополнить базу студентов - отправьте фото студента, а также заполните краткую '
                        'о нем')


@dp.message_handler(commands=['Отмена'], state='*')
async def run_command_cancel(message: types.Message, state=FSMContext):
    await state.finish()
    await run_command(message.from_user.id)


@dp.message_handler(commands=['Начать'])
async def run_command_memorize(message: types.Message):
    await message.answer('Выберите студентов какого курса вы хотите запомнить.',
                         reply_markup=keyboards.greet_memorize_course())
    await stm.memorize.memorize_course.set()


@dp.message_handler(state=stm.memorize.memorize_course)
async def memorize_course(message: types.Message):
    globals()['course' + str(message.from_user.id)] = message.text
    if globals()['course' + str(message.from_user.id)] == "Все":
        globals()['course' + str(message.from_user.id)] = 0
    elif globals()['course' + str(message.from_user.id)] in ['1', '2', '3', '4']:
        globals()['course' + str(message.from_user.id)] = int(globals()['course' + str(message.from_user.id)])
    else:
        await message.answer('Некорректный выбор. Выберите курс из предложенных вариантов.')
        return False
    if db.check_empty_course(globals()['course' + str(message.from_user.id)]):
        await message.answer('К сожалению, студентов данного курса нет в базе, выберите другой курс.')
        return False
    await send_photo(message.from_user.id)


async def send_photo(chat_id):
    photo = db.get_photo(globals()['course' + str(chat_id)])
    globals()['correct_answer' + str(chat_id)] = photo[1]
    sex = photo[2]
    greet = keyboards.create_greet(chat_id, globals()['correct_answer' + str(chat_id)], sex)
    await bot.send_photo(chat_id=chat_id, photo=open(photo[0], 'rb'), reply_markup=greet)
    await stm.memorize.answer.set()


@dp.message_handler(state=stm.memorize.answer)
async def check_answer(message: types.Message):
    answer = message.text
    if answer == globals()['correct_answer' + str(message.from_user.id)]:
        await message.answer("Правильно!")
    else:
        await message.answer(
            'Неправильно, правильный ответ: ' + globals()['correct_answer' + str(message.from_user.id)])
    await send_photo(message.from_user.id)


@dp.message_handler(commands=['Пополнить'])
async def run_command_add(message: types.Message):
    await message.reply('Отправьте фото студента', reply_markup=keyboards.greet_cancel())
    await stm.fill_up.photo.set()


@dp.message_handler(content_types=['photo'], state=stm.fill_up.photo)
async def download_photo(message: types.Message):
    file = 'photos/' + str(message.from_user.id) + '.jpg'
    await message.photo[-1].download(file)
    success = imaginate(file)
    if success == 0:
        await message.answer('На фото не обнаружено лица, отправьте другое фото')
        return False
    if success == 2:
        await message.answer('На фото обнаружено более одного лица, отправьте другое фото')
        return False
    await send_photo_after_proc(message.from_user.id)


async def send_photo_after_proc(chat_id):
    await bot.send_photo(chat_id, photo=open('photos/' + str(chat_id) + '.jpg', 'rb'))
    await bot.send_message(chat_id, 'Вас устроит такая обработка фото?',
                           reply_markup=keyboards.greet_test_photo())
    await stm.fill_up.test_photo.set()


@dp.message_handler(state=stm.fill_up.test_photo)
async def test_photo(message: types.Message):
    yes_or_not = message.text
    if yes_or_not == 'Да':
        await message.answer('Введите фамилию и имя студента на русском языке через пробел.',
                             reply_markup=keyboards.greet_cancel())
        await stm.fill_up.name.set()
    elif yes_or_not == 'Нет':
        await message.answer('Отправьте другое фото.',
                             reply_markup=keyboards.greet_cancel())
        await stm.fill_up.photo.set()
    else:
        await message.answer('Некорректный ввод расценивается как "Нет". Отправьте другое фото.',
                             reply_markup=keyboards.greet_cancel())
        await stm.fill_up.photo.set()


@dp.message_handler(content_types=ContentType.ANY, state=stm.fill_up.photo)
async def incorrect_photo(message: types.Message):
    await message.answer("Это не формат фото, отправьте фотографию.")


@dp.message_handler(state=stm.fill_up.name)
async def get_name(message: types.Message):
    globals()['sex' + str(message.from_user.id)] = 0
    globals()['student_name' + str(message.from_user.id)] = str(message.text)
    if len(globals()['student_name' + str(message.from_user.id)].split()) != 2:
        await message.answer("Некорректный ввод.\nУбедитесь, что вы ввели фамилию и имя через пробел.")
        return False
    surname, name = str(message.text).split()
    check_result = utils.check_name(name)
    if not check_result:
        await message.answer("Проверьте корректность имени, в базе из 51530 имен не найдено данное.")
        return False
    else:
        globals()['sex' + str(message.from_user.id)] = check_result
    await message.answer("Введите курс студента.",
                         reply_markup=keyboards.greet_course())
    await stm.fill_up.course.set()


@dp.message_handler(state=stm.fill_up.course)
async def get_course(message: types.Message, state=FSMContext):
    file = 'photos/' + str(message.from_user.id) + '.jpg'
    if message.text not in ['1', '2', '3', '4']:
        await message.answer("Проверьте, что вы верно указали номер курса.")
        return False
    db.add_photo(globals()['student_name' + str(message.from_user.id)], message.text,
                 globals()['sex' + str(message.from_user.id)], file)
    await message.answer("Студент успешно добавлен.")
    await state.finish()
    await run_command(message.from_user.id)


@dp.message_handler(content_types=ContentType.ANY)
async def process_anyway_after_start(message: types.Message):
    await message.answer('Некорректный ввод, выберите из предложенных вариантов.')


if __name__ == '__main__':
    executor.start_polling(dp)
