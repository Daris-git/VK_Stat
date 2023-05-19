from tkinter import *
from tkinter import simpledialog
from tkinter import ttk


functions = ["help", "login", "set_group_id", "non_active_users", "get_banned_or_deleted", 
             "check_two_groups", "most_popular_posts", "group_info", "exit"]


root = Tk()
root.geometry("700x600")
root.title("VK Stat")
root.resizable(False, False)

exe_icon = PhotoImage(file="button_exe_icon.png")

Group_ID = 0
First_Name = "First"
Last_Name = "Last"


menubar = Menu(root)
menubar.add_command(label=First_Name + " " + Last_Name)
menubar.add_command(label="Помощь")
menubar.add_command(label="О программе")

root.config(menu=menubar)


button = Button(root,text="Начать", image=exe_icon, border=0) 

textArea = Text(root, fg="#FFFFFF", bg="#3F3F3F", font=("Inter", 10), height = 10, width = 70)

functionList = ttk.Combobox(values = functions, justify="left")
functionList.current(0)

groupIdLabel = Label(text="ID группы:" + str(Group_ID), bg="#DCDCDC", fg="#000000", font=("Inter", 10), width=20, justify="left")




functionList.place(x = 40, y = 95)
groupIdLabel.place(x = 470, y = 95)
button.place(x = 225, y = 260)
textArea.place(x = 32, y = 340)


# login_input = simpledialog.askstring("VK Stat", "Введите ваш логин", parent=root)
# password_input = simpledialog.askstring("VK Stat", "Введите ваш логин", parent=root, show = "*")



root.mainloop()

