import os
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from actions import *
from bd import *


# Токен доступа сообщества
token = 'vk1.a.O4dXjWDu03bh6OF-7LEiIJLBYEmhoEBQPIsR0GMjLIbRdO0Uun8KCc_g5sL0DTftDgonIkar2Paq7_SLUQeyZN1YIlF19mEVQ2I-w22oMgBsTr8DZTUQ7irP-J600kJNCBgIVh0a53Q161YlddbcnGzuZXU7UH9NB_ksit89djS1L6KjSfuTenFgs3tMg7MHoidgrhBqpXMHtloAlYhBoQ'

# Авторизация бота
vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
user = None


# Основной цикл обработки сообщений
def listen_for_events():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user = nm.get_vkid(str(event.user_id))
            user_message = event.text.lower()
            print(user)
            if user:
                if user[-1] == 0:
                    flag = find_value_in_excel(user_message)
                    #flag = nm.get_vkid(str(event.user_id))
                    if flag:
                        nm.set_name(user[5], user_message)
                        send_message(vk_session, event.peer_id, registr[1])
                    else:
                        send_message(vk_session, event.peer_id, registr[-1])
                elif user[-1] == 1:
                    nm.set_obshaga(user[5], user_message)
                    send_message(vk_session, event.peer_id, registr[2])
                elif user[-1] == 2:
                    nm.set_date(user[5], user_message)
                    send_message(vk_session, event.peer_id, registr[3])
                else:
                    send_message(vk_session, event.peer_id, 'Вы зарегистрированы')
                    if user[1] == '1':
                        keyboard = create_keyboard(6)
                        send_message(vk_session, event.peer_id, 'У вас права администратора', keyboard)

                        if user_message == commands_list_admin_begin[0]:
                            keyboard = create_keyboard(7)
                            send_message(vk_session, event.peer_id, 'Выберите действие с администраторами', keyboard)
                            send_message(vk_session, event.peer_id, 'Тут будет список действующих админов', keyboard)

                        elif user_message == commands_list_admin_begin[1]:
                            keyboard = create_keyboard(8)
                            send_message(vk_session, event.peer_id, 'Выберите действие с заведущими', keyboard)
                            send_message(vk_session, event.peer_id, 'Тут будет список действующих заведущих', keyboard)

                        elif user_message == commands_list_admin_admin[0]:
                            send_message(vk_session, event.peer_id, 'Пришлите id пользователя, которому нужно выдать права администратора')
                            #сделать последнее активное действие на добавление админа и запустить функцию

                        elif user_message == commands_list_admin_admin[1]:
                            send_message(vk_session, event.peer_id, 'Напишите номер админа из списка, у которого нужно отобрать админские права')
                            #так же сделать последнее активное действие на удаление

                        elif user_message == commands_list_admin_admin[2]:
                            keyboard = create_keyboard(6)
                            send_message(vk_session, event.peer_id, 'У вас права администратора', keyboard)

                        elif user_message == commands_list_admin_comenda[0]:
                            send_message(vk_session, event.peer_id, 'Пришлите id пользователя, которому нужно выдать права заведущий')
                            #сделать последнее активное действие на добавление заведущей и запустить функцию

                        elif user_message == commands_list_admin_comenda[1]:
                            send_message(vk_session, event.peer_id, 'Напишите номер админа из списка, у которого нужно отобрать админские права')
                            #так же сделать последнее активное действие на удаление

                        elif user_message == commands_list_admin_comenda[2]:
                            keyboard = create_keyboard(5)
                            send_message(vk_session, event.peer_id, 'Меню коменды через администратора', keyboard)

                        elif user_message == commands_list_admin_comenda[3]:
                            keyboard = create_keyboard(6)
                            send_message(vk_session, event.peer_id, 'Меню администратора', keyboard)

                    elif user[1] == '2':
                        keyboard = create_keyboard(5)
                        send_message(vk_session, event.peer_id, 'У вас права заведущей', keyboard)
                        if user_message == commands_list_comenda[0]:
                            ...
                        if user_message == commands_list_comenda[1]:
                            ...
                        if user_message == commands_list_comenda[2]:
                            ...
                        if user_message == commands_list_comenda[3]:
                            ...

                    elif user[1] == '0':
                        keyboard = create_keyboard(1)
                        send_message(vk_session, event.peer_id, 'У вас права проживающего', keyboard)
                        if user_message == commands_list_all[0]:
                            ...
                        elif user_message == commands_list_all[1]:
                            ...
                        elif user_message == commands_list_all[2]:
                            ...
            else: #регистрация
                nm.insert(str(event.user_id))
                send_message(vk_session, event.peer_id, registr[0])


# Запуск Flask приложения
if __name__ == '__main__':
    from threading import Thread

    # Запуск прослушивания событий VK в отдельном потоке
    Thread(target=listen_for_events).start()

