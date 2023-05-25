from tkinter import *
from tkinter import simpledialog
from tkinter import ttk
from tkinter import messagebox as mb
import time
import traceback
import logging
import VK_Stat_GUI as VKS


functions = ["help", "login", "set_group_id", "non_active_users", "get_banned_or_deleted", 
             "check_two_groups", "most_popular_posts", "group_info", "exit", "clear_console"]

program_name = "VK Stat v.1.0"


root = Tk()
root.geometry("700x600")
root.title(program_name)
root.resizable(False, False)

exe_icon = PhotoImage(file="button_exe_icon.png")

welcome_mb = True

Group_ID = 0
First_Name = "First"
Last_Name = "Last"

selected_function = "help"


textArea = Text(root, fg="#FFFFFF", bg="#3F3F3F", font=("Inter", 10), height = 10, width = 70, state=DISABLED)


def input_group_id():
    group_input = simpledialog.askstring(program_name, "Введите ID группы", parent=root)
    get_id = VKS.set_group_id(group_input)

    if get_id[0] == True:
        return get_id
    
    return [0, 0]



def login_gui():

    while(True):

        login_input = simpledialog.askstring(program_name, "Введите ваш логин", parent=root)
        if login_input == None: exit()

        password_input = simpledialog.askstring(program_name, "Введите ваш пароль", show = "*", parent=root)
        if password_input == None: exit()


        try:
            VKS.vk_auth(login_input, password_input)
            first_Name = VKS.vk.users.get()[0]['first_name']
            last_Name = VKS.vk.users.get()[0]['last_name']
            return (first_Name, last_Name)
        except Exception as e:
            logging.error(traceback.format_exc())



def log_out():
    logout_answer = mb.askyesno(title=program_name, message="Выйти из аккаунта?")

    if logout_answer: First_Name, Last_Name = login_gui()


def menu_help():
    mb.showinfo(program_name, "Если программа выдала ошибку или возникли другие вопросы" + "\n" + "Напишите разработчику в Discord:Daris#6534")


def menu_info():
    mb.showinfo(program_name, program_name + "\n" + "Многофункциональная программа для получение статистики и иной информации о сообществе в VK")



def execute_function(func):
    global Group_ID

    if func == "clear_console":
        textArea.config(state=NORMAL) 
        textArea.delete('1.0', END)
        textArea.config(state=DISABLED) 

    if func == "exit":
        if mb.askyesno(title=program_name, message="Выйти из программы?"): exit()

    if func == "help":
        textArea.config(state=NORMAL) 
        textArea.insert(END, VKS.help())
        textArea.insert(END, '\n' + "" + '\n')
        textArea.config(state=DISABLED)

    if func == "group_info":
        get_func = VKS.group_info(Group_ID)
        if get_func[0]:
            textArea.config(state=NORMAL) 
            textArea.insert(END, "Информация о группе" + '\n')
            textArea.insert(END, get_func[1])
            textArea.insert(END, '\n' + "" + '\n')
            textArea.config(state=DISABLED)

    if func == "set_group_id": 
        get_id = input_group_id()
        if get_id != [0, 0]:
            print(get_id)
            Group_ID = get_id[1]
            groupIdLabel.config(text="ID группы:" + str(Group_ID))
            textArea.config(state=NORMAL) 
            textArea.insert(END, "ID группы подтвержден" + '\n')
            textArea.insert(END, get_id[2])
            textArea.insert(END, '\n' + "" + '\n')
            textArea.config(state=DISABLED)



# First_Name, Last_Name = login_gui()
# Group_ID = input_group_id()[1]


menubar = Menu(root)


menubar_user = Menu(menubar)
menubar_user.add_command(label="Выйти", command=log_out)

menubar.add_cascade(label=First_Name + " " + Last_Name, menu=menubar_user)
menubar.add_command(label="Помощь", command=menu_help)
menubar.add_command(label="О программе", command=menu_info)

root.config(menu=menubar)


button = Button(root,text="Начать", image=exe_icon, border=0, command=lambda: execute_function(functionList.get())) 


functionList = ttk.Combobox(values = functions, justify="left")
functionList.current(0)

groupIdLabel = Label(text="ID группы:" + str(Group_ID), bg="#DCDCDC", fg="#000000", font=("Inter", 10), width=20, justify="left")




functionList.place(x = 40, y = 95)
groupIdLabel.place(x = 470, y = 95)
button.place(x = 225, y = 260)
textArea.place(x = 32, y = 340)




root.mainloop()

