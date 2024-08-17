# модули для работы с сообщениями ВК
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from bd import *
import requests
import os
import xlrd

db = DB()
nm = UserModel(db.get_connection())

USERS = ['student', 'admin', 'comenda']
commands_list_begin = ['регистрация', 'задать вопрос']
registr = ['Здравствуйте, Введите своё ФИО для регистрации', 'Введите номер общежития', 'Введите дату рождения в формате 00.00.0000', 'Вы успешно прошли регистрацию', 'Вы не прошли регистрацию. Проверьте правильность введёных Вами данных.']
commands_list_all = ['Оплата общежития', 'Обработака', 'Задать вопрос']
commands_list_comenda = ['Загрузить информацию о долгах', 'Загрузить информацию о проживающих', 'Отправить уведомление', 'Задать вопрос']
commands_list_payment = ['Загрузить чек', 'Инструкция об оплате', 'Меню']
commands_list_clean_type = ['Клопы', 'Тараканы', 'Меню']
commands_list_clean = ['Записать комнату', 'Отменить запись', 'Меню']
commands_list_admin_begin = ['Управление заведущими', 'Управление админами']
commands_list_admin_comenda = ['Выдать роль заведущей', 'Убрать роль заведущей', 'Открыть меню заведущей', 'Меню']
commands_list_admin_admin = ['Выдать роль админу', 'Убрать роль админа', 'Меню']


def send_message(vk_session: vk_api.vk_api.VkApi, peer_id, message, keyboard=None):
    vk_session.method('messages.send', {
        'peer_id': peer_id,
        'message': message,
        'random_id': 0,
        'keyboard': keyboard
    })


def download_file(url, filename):
    response = requests.get(url)
    with open(os.path.join('uploads', filename), 'wb') as file:
        file.write(response.content)


def find_value_in_excel(search_value):
    # Загрузка рабочей книги
    df = xlrd.open_workbook('uploads/проживающие в номерном фонде (1).xlsx')
    sheet = df.sheet_by_index(0)
    search_value = ''.join(search_value.split(' ')).lower()
    # Проход по всем строкам и столбцам
    for row_idx in range(sheet.nrows):
        for col_idx in range(sheet.ncols):
            cell_value = sheet.cell_value(row_idx, col_idx)
            cell_value = ''.join(str(cell_value).split(' ')).lower()
            if cell_value == search_value:
                return (row_idx, col_idx)
    return None


def send_doc_for_data(event, vk_session: vk_api.vk_api.VkApi):
    attachments = event.attachments
    if 'attach1' in attachments and 'attach1_type' in attachments:
        attachment_type = attachments['attach1_type']
        if attachment_type == 'doc':
            doc_id_key = 'attach1'
            if doc_id_key in attachments:
                doc = \
                vk_session.method('messages.getById', {'message_ids': event.message_id})['items'][0]['attachments'][0][
                    'doc']
                if doc['ext'] == 'xlsx':
                    download_file(doc['url'], doc['title'])
                    send_message(event.peer_id, f'Файл {doc['title']} успешно загружен.')
                else:
                    send_message(event.peer_id, 'Поддерживаются только файлы с расширением .xlsx')
            else:
                send_message(event.peer_id, 'Не удалось получить информацию о файле.')
        else:
            send_message(event.peer_id, 'Прикрепленный файл не является документом.')
    else:
        send_message(event.peer_id, 'Нет прикрепленных файлов.')


def create_keyboard(response: int) -> VkKeyboard:
    ''' Возвращает пользователю сформированную клавиатуру.

        Аргументы:
            response: int - запрос, который отправляет пользователь

        Возвращает:
            VkKeyboard - сформированную клавиатуру, которую запросил пользователь
    '''

    keyboard = VkKeyboard(one_time=False)

    if response == 0:
        keyboard.add_button(commands_list_begin[0], color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(commands_list_begin[1], color=VkKeyboardColor.POSITIVE)

    elif response == 1:
        keyboard.add_button(commands_list_all[0], color=VkKeyboardColor.POSITIVE)
        keyboard.add_button(commands_list_all[1], color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(commands_list_all[2], color=VkKeyboardColor.POSITIVE)

    elif response == 2:
        keyboard.add_button(commands_list_payment[0], color=VkKeyboardColor.POSITIVE)
        keyboard.add_button(commands_list_payment[1], color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(commands_list_payment[2], color=VkKeyboardColor.POSITIVE)

    elif response == 3:
        keyboard.add_button(commands_list_clean[0], color=VkKeyboardColor.POSITIVE)
        keyboard.add_button(commands_list_clean[1], color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(commands_list_clean[2], color=VkKeyboardColor.POSITIVE)

    elif response == 4:
        keyboard.add_button(commands_list_clean_type[0], color=VkKeyboardColor.POSITIVE)
        keyboard.add_button(commands_list_clean_type[1], color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(commands_list_clean_type[2], color=VkKeyboardColor.POSITIVE)

    elif response == 5:
        keyboard.add_button(commands_list_comenda[0], color=VkKeyboardColor.POSITIVE)
        keyboard.add_button(commands_list_comenda[1], color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(commands_list_comenda[2], color=VkKeyboardColor.POSITIVE)
        keyboard.add_button(commands_list_comenda[3], color=VkKeyboardColor.POSITIVE)

    elif response == 6:
        keyboard.add_button(commands_list_admin_begin[0], color=VkKeyboardColor.POSITIVE)
        keyboard.add_button(commands_list_admin_begin[1], color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(commands_list_admin_begin[2], color=VkKeyboardColor.POSITIVE)

    elif response == 7:
        keyboard.add_button(commands_list_admin_admin[0], color=VkKeyboardColor.POSITIVE)
        keyboard.add_button(commands_list_admin_admin[1], color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(commands_list_admin_admin[2], color=VkKeyboardColor.POSITIVE)

    elif response == 8:
        keyboard.add_button(commands_list_admin_comenda[0], color=VkKeyboardColor.POSITIVE)
        keyboard.add_button(commands_list_admin_comenda[1], color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(commands_list_admin_comenda[2], color=VkKeyboardColor.POSITIVE)
        keyboard.add_button(commands_list_admin_comenda[3], color=VkKeyboardColor.POSITIVE)

    keyboard = keyboard.get_keyboard()
    return keyboard