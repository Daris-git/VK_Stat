import traceback
import logging
import getpass
import vk_api

from datetime import datetime
from tkinter import simpledialog
from tkinter import messagebox as mb



""" При двухфакторной аутентификации вызывается эта функция. """
def auth_handler():
    key = simpledialog.askstring("VK Stat", "Введите код аутентификации")
    remember_device = True

    return key, remember_device




def vk_auth(login, password):
    global vk_session
    global vk

    vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)
    vk_session.auth()

    vk = vk_session.get_api()



def set_group_id(GROUP_ID_input):
    global GROUP_ID

    GROUP_ID = 0


    try:
        test_group = vk.groups.getMembers(group_id = GROUP_ID_input)
        group_info = vk.groups.getById(group_id = GROUP_ID_input)
        return (True, GROUP_ID_input, group_info[0]['name'])
    except Exception as e:
        return (False, str(logging.error(traceback.format_exc())) + "\n" + "Ошибка!" + 
                "\n" + "Проверьте правильность введенных данных или свяжитесь с разработчиком")



def group_info(g_id):

    try:
        group_inf = vk.groups.getById(group_id = g_id)
        return (True, group_inf[0]['name'])
    except Exception as e:
        return (False, str(logging.error(traceback.format_exc())) + "\n" + "Ошибка!" + 
                "\n" + "Проверьте правильность введенных данных или свяжитесь с разработчиком")
    

def get_banned_or_deleted(g_id):

    

    return False



def help():
    return ("login - войти в другой аккаунт" + "\n" + 
            "set_group_id - установить новый id группы" + "\n" + 
            "non_active_users - получение списка неактивных пользователей группы" + "\n" + 
            "get_banned_or_deleted - получение списка удаленных или забаненных пользователей" + "\n" + 
            "check_two_groups - сравнение списка подписчиков двух групп (сравнение по прицепу подписки)" + "\n" + 
            "most_popular_posts - Получить список самых популярных постов в группе" + "\n" + 
            "group_info - получить информацию о текущей группе" + "\n" + 
            "exit - выход из программы")






