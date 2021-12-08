import socket
import threading
import json
import tkinter
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText


IP = ''
PORT = ''
user = ''
# user list box
listbox1 = ''
# 是否開關user listf
ii = 0
# user list
users = []
chat = '------Group chat-------'
# Log in 的視窗
root1 = tkinter.Tk()
root1.title('Log in')
root1['height'] = 110
root1['width'] = 270
root1.resizable(0, 0)

# ip和port
IP1 = tkinter.StringVar()
IP1.set('127.0.0.1:50007')
User = tkinter.StringVar()
User.set('')

# server label
labelIP = tkinter.Label(root1, text='Server address')
labelIP.place(x=20, y=10, width=100, height=20)

entryIP = tkinter.Entry(root1, width=80, textvariable=IP1)
entryIP.place(x=120, y=10, width=130, height=20)

# username label
labelUser = tkinter.Label(root1, text='Username')
labelUser.place(x=30, y=40, width=80, height=20)

entryUser = tkinter.Entry(root1, width=80, textvariable=User)
entryUser.place(x=120, y=40, width=130, height=20)


# login button
def login(*args):
    global IP, PORT, user
    # get ip and port
    IP, PORT = entryIP.get().split(':')
    PORT = int(PORT)
    user = entryUser.get()
    # 判斷使用者名稱是否為空
    if not user:
        tkinter.messagebox.showerror(
            'Name type error', message='Username Empty!')
    else:
        root1.destroy()


# 把login功能寫入tkinter的button中
root1.bind('<Return>', login)
but = tkinter.Button(root1, text='Log in', command=login)
but.place(x=100, y=70, width=70, height=30)

root1.mainloop()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
if user:
    # send user name
    s.send(user.encode())
else:
    # no user name
    s.send('no'.encode())

# 如果沒有user name就會把ip和port設為user name
addr = s.getsockname()  # get ip and username
addr = addr[0] + ':' + str(addr[1])
if user == '':
    user = addr

# Chat room GUI
root = tkinter.Tk()
root.title(user)  # 把聊天室名稱命名為使用者名稱
root['height'] = 400
root['width'] = 580
root.resizable(0, 0)

# 创建多行文本框
listbox = ScrolledText(root)
listbox.place(x=5, y=0, width=570, height=320)
# 文本框使用的字体颜色
listbox.tag_config('red', foreground='#FF0000')
listbox.tag_config('blue', foreground='#2365a6')
listbox.tag_config('green', foreground='#007500')
listbox.tag_config('black', foreground='#000000')
listbox.insert(tkinter.END, 'Welcome to the chat room!', '#000000')

# Emoji
# 四個按鈕
b1 = ''
b2 = ''
b3 = ''
b4 = ''
# emoji圖片 resize成70*70
emoji_1 = tkinter.PhotoImage(file='./emoji/thinking-face.png')
emoji_2 = tkinter.PhotoImage(file='./emoji/sunglasses.png')
emoji_3 = tkinter.PhotoImage(file='./emoji/rolling-eyes.png')
emoji_4 = tkinter.PhotoImage(file='./emoji/money-mouth-face.png')

# 做成字典一一對應
dict = {'aa**': emoji_1, 'bb**': emoji_2, 'cc**': emoji_3, 'dd**': emoji_4}
ee = 0  # 判斷emoji的GUI是否被打開


# 點emoji之後就會發送emoji
# exp是emoji
def mark(exp):
    global ee
    mes = exp + ':;' + user + ':;' + chat
    s.send(mes.encode())
    b1.destroy()
    b2.destroy()
    b3.destroy()
    b4.destroy()
    ee = 0


# 對應emoji的function
def bb1():
    mark('aa**')


def bb2():
    mark('bb**')


def bb3():
    mark('cc**')


def bb4():
    mark('dd**')


def express():
    global b1, b2, b3, b4, ee
    if ee == 0:
        ee = 1
        b1 = tkinter.Button(root, command=bb1, image=emoji_1,
                            relief=tkinter.FLAT, bd=0)
        b2 = tkinter.Button(root, command=bb2, image=emoji_2,
                            relief=tkinter.FLAT, bd=0)
        b3 = tkinter.Button(root, command=bb3, image=emoji_3,
                            relief=tkinter.FLAT, bd=0)
        b4 = tkinter.Button(root, command=bb4, image=emoji_4,
                            relief=tkinter.FLAT, bd=0)

        b1.place(x=5, y=248)
        b2.place(x=75, y=248)
        b3.place(x=145, y=248)
        b4.place(x=215, y=248)
    else:
        ee = 0
        b1.destroy()
        b2.destroy()
        b3.destroy()
        b4.destroy()


# emoji button
eBut = tkinter.Button(root, text='emoji', command=express)
eBut.place(x=5, y=320, width=60, height=30)


# Online user list
listbox1 = tkinter.Listbox(root)
listbox1.place(x=445, y=0, width=130, height=320)


def users():
    global listbox1, ii
    if ii == 1:
        listbox1.place(x=445, y=0, width=130, height=320)
        ii = 0
    else:
        # 隱藏controller
        listbox1.place_forget()
        ii = 1


# online user list button
button1 = tkinter.Button(root, text='Online users', command=users)
button1.place(x=485, y=320, width=90, height=30)

# Input Text box
a = tkinter.StringVar()
a.set('')
entry = tkinter.Entry(root, width=120, textvariable=a)
entry.place(x=5, y=350, width=570, height=40)

# Send message


def send(*args):
    users.append('------Group chat-------')
    print(chat)
    # 如果users中沒東西會提示沒人可以跟你聊天 你是宇宙邊緣人
    if chat not in users:
        tkinter.messagebox.showerror(
            'Send error', message='There is nobody to talk to!')
        return
    if chat == 'Robot':
        print('Robot')
    if chat == user:
        tkinter.messagebox.showerror(
            'Send error', message='Cannot talk with yourself in private!')
        return
    # 跟誰講話
    mes = entry.get() + ':;' + user + ':;' + chat
    s.send(mes.encode())
    a.set('')  # 發送訊息後清空textbox


# Send message button
button = tkinter.Button(root, text='Send', command=send)
button.place(x=515, y=353, width=60, height=30)
root.bind('<Return>', send)


# 私訊功能
def private(*args):
    global chat
    # Get user name
    indexs = listbox1.curselection()
    index = indexs[0]
    if index > 0:
        chat = listbox1.get(index)
        # 把Group chat改成private chat
        if chat == '------Group chat-------':
            root.title(user)
            return
        ti = user + '  -->  ' + chat
        root.title(ti)


# 在user list上綁定私訊
listbox1.bind('<ButtonRelease-1>', private)


# Receive message
def recv():
    global users
    while True:
        data = s.recv(1024)
        data = data.decode()
        # 如果沒有error表示收到user list
        try:
            data = json.loads(data)
            users = data
            # clean user list box
            listbox1.delete(0, tkinter.END)
            number = ('   Users online: ' + str(len(data)))
            listbox1.insert(tkinter.END, number)
            listbox1.itemconfig(tkinter.END, fg='green', bg="#f0f0ff")
            listbox1.insert(tkinter.END, '------Group chat-------')
            listbox1.itemconfig(tkinter.END, fg='green')
            for i in range(len(data)):
                listbox1.insert(tkinter.END, (data[i]))
                listbox1.itemconfig(tkinter.END, fg='green')
        except:
            data = data.split(':;')
            data1 = data[0].strip()  # 發送的訊息
            data2 = data[1]  # user name
            data3 = data[2]  # 聊天對象
            if 'INVITE' in data1:
                if data3 == '------Group chat-------':
                    tkinter.messagebox.showerror(
                        'Connect error', message='Group video chat is not supported!')
                continue
            markk = data1.split('：')[1]
            # 判斷是不是圖片
            pic = markk.split('#')
            # 判斷是不是表情
            # 如果字典中有emoji
            if (markk in dict) or pic[0] == '``':
                data4 = '\n' + data2 + '：'  # 名字-> \n名字：
                if data3 == '------Group chat-------':
                    if data2 == user:
                        # 如果是自己則把字體變成藍色
                        listbox.insert(tkinter.END, data4, 'blue')
                    else:
                        listbox.insert(tkinter.END, data4,
                                       'green')
                elif data2 == user or data3 == user:  # 私聊
                    listbox.insert(tkinter.END, data4, 'red')
                if pic[0] != '``':
                    # 把emoji傳到聊天室
                    listbox.image_create(tkinter.END, image=dict[markk])
            # 字體顏色設定
            else:
                data1 = '\n' + data1
                if data3 == '------Group chat-------':
                    if data2 == user:
                        # 如果是自己則把字體變成藍色
                        listbox.insert(tkinter.END, data1, 'blue')
                    else:
                        listbox.insert(tkinter.END, data1,
                                       'green')
                    if len(data) == 4:
                        listbox.insert(tkinter.END, '\n' + data[3], 'black')
                elif data2 == user or data3 == user:  # private chat
                    listbox.insert(tkinter.END, data1, 'red')
            listbox.see(tkinter.END)  # 顯示在最後


# Start receive message
r = threading.Thread(target=recv)
r.start()
# Tkinter GUI
root.mainloop()
s.close()
