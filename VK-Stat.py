import traceback
import logging
import getpass
import vk_api

user_is_logged = False

START_POST_ID = 18840

def vk_auth(login, password):
    global vk_session
    global vk

    LOGIN = login
    PASSWORD = password

    vk_session = vk_api.VkApi(login, password)
    vk_session.auth()

    vk = vk_session.get_api()


banned_or_deleted_users = []
banned_or_deleted_users_id = []
posts = []
users = []
users_id = []
active_users = []


def set_group_id():
    global GROUP_ID 

    GROUP_ID = 0

    while(True):
        print("Для отмены опеарции введите 'exit'")

        inp_group = input("Введите id группы (цифры):")

        if inp_group.lower() == "exit": return True

        try:
            test_group = vk.groups.getMembers(group_id = inp_group)
            group_info = vk.groups.getById(group_id = inp_group)
            print("ID группы подтвержден")
            print(group_info[0]['name'])
            user_is_logged = True
            break
        except Exception as e:
            logging.error(traceback.format_exc())
            print("Ошибка!")
            print("Проверьте правильность введенных данных или свяжитесь с разработчиком")

    GROUP_ID = inp_group




def login():

    LOGIN = ""
    PASSWORD = ""

    while(True):
        print("Для отмены опеарции введите 'exit'")

        inp_login = input("Введите логин (номер телефона или почта):")

        if inp_login.lower() == "exit": break

        print("Введите пароль")
        inp_password = getpass.getpass()
        
        try:
            vk_auth(inp_login, inp_password)
            print("Авторизация завершена")
            break
        except Exception as e:
            logging.error(traceback.format_exc())
            print("Ошибка!")
            print("Проверьте правильность введенных данных или свяжитесь с разработчиком")



def get_all_users_id():

    group_users = vk.groups.getMembers(group_id = GROUP_ID)
    list_mem = group_users['items']
    users = vk.users.get(user_ids = list_mem)

    global users_id
    
    users_id = []
    
    for j in users:
        users_id.append(j['id'])



def get_all_posts_id():
    g_id = "-" + GROUP_ID
    group_wall = vk.wall.get(owner_id = g_id)


    posts_count = group_wall['count']
    n = 0

    print("Получение списка всех постов группы...")

    while(posts_count > 0):
        group_wall = vk.wall.get(owner_id = g_id, offset = n, count = 100)
        all_posts = group_wall['items']


        for i in all_posts:
            
            if(i['id'] == START_POST_ID):
                posts_count = -1
                break

            posts.append(i['id'])

        posts_count = posts_count - 100
        n = n + 100

    print("Операция завершена. Список получен")


def get_banned_and_deleted_accounts():

    group_users = vk.groups.getMembers(group_id = GROUP_ID)

    list_mem = group_users['items']

    users = vk.users.get(user_ids = list_mem)

    for user in users:
        if len(user) == 6:
            banned_or_deleted_users.append(user['first_name'] + " " + user['last_name'])
            banned_or_deleted_users_id.append(str(user['id']))

    print("Колличество пользователей:" + str(len(banned_or_deleted_users)))
    for i in range(len(banned_or_deleted_users)): print(banned_or_deleted_users[i] + " https://vk.com/id" + banned_or_deleted_users_id[i])



def group_info():

    group_inf = vk.groups.getById(group_id = GROUP_ID)
    print("Информация о группе")
    print(group_inf[0]['name'])


def non_active_users():

    g_id = "-" + GROUP_ID

    if(len(posts) == 0): get_all_posts_id()
    if(len(users_id) == 0): get_all_users_id()

    group_users = vk.groups.getMembers(group_id = GROUP_ID)
    list_mem = group_users['items']
    users = vk.users.get(user_ids = list_mem)


    for id in posts:
        post_likes = vk.wall.getLikes(owner_id = g_id, post_id = id)['users']
        
        for like_id in post_likes:
            if like_id['uid'] not in active_users and like_id['uid'] in users_id:
                active_users.append(like_id['uid'])



    print("Колличество пользователей:" + str(len(users)))    
    print("Колличество активных пользователей:" + str(len(active_users)))


    for user in users:
        if user['id'] not in active_users:
            print(user['first_name'] + " " + user['last_name'] + " https://vk.com/id" + str(user['id']))

    



print("Чтобы пользоватся командами необходи пройти авторизацию в VK API, для прохождения авторизации напишете команду - login")
print("В случае ошибки свяжитесь с разработчиком")


if login() or set_group_id(): exit()


print("Добро пожаловать в VK Stat, для получения списка комманды введите 'help'")

try:
    while(True):
        inp = input("> ")
        if inp.lower() == "help":
            print("login - войти в другой аккаунт")
            print("set_group_id - установить новый id группы")
            print("non_active_users - получение списка неактивных пользователей группы")
            print("get_banned_or_deleted - получение списка удаленных или забанненых пользователей")
            print("group_info - получить информацию о текущей группе")
            print("exit - выход из программы")
        
        if inp.lower() == "non_active_users":
            non_active_users()

        if inp.lower() == "get_banned_or_deleted":
            get_banned_and_deleted_accounts()

        if inp.lower() == "set_group_id":
            set_group_id()

        if inp.lower() == "group_info":
            group_info()

        if inp.lower() == "login":
            login()

        if inp.lower() == "exit":
            break

except Exception as e:
    logging.error(traceback.format_exc())
    print("Ошибка!")
    print("Свяжитесь с разработчиком")



