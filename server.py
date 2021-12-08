import socket
import threading
import queue
import json
import time
import os
import os.path
import sys

IP = ''
PORT = 50007
queue = queue.Queue()                   # 存client端傳過來的訊息
users = []                              # 存線上使用者的訊息  [conn, user, addr]
lock = threading.Lock()                 # multitreading lock

# client連接到聊天室之後加入到user list中


def onlines():
    online = []
    for i in range(len(users)):
        online.append(users[i][1])
    return online


class ChatServer(threading.Thread):
    global users, queue, lock

    def __init__(self, port):
        threading.Thread.__init__(self)
        # self.setDaemon(True)
        self.ADDR = ('', port)
        # self.PORT = port
        os.chdir(sys.path[0])
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.conn = None
        # self.addr = None

    # 接收client端發送的訊息
    def tcp_connect(self, conn, addr):
        # 接收user name
        user = conn.recv(1024)
        user = user.decode()

        # 確認使用者是否已經在user list中
        for i in range(len(users)):
            if user == users[i][1]:
                print('User already exist')
                user = '' + user + '_2'

        if user == 'no':
            user = addr[0] + ':' + str(addr[1])
        users.append((conn, user, addr))
        # Print new user name
        print(' New connection:', addr, ':', user, end='')
        # refresh user list
        d = onlines()
        self.recv(d, addr)
        try:
            while True:
                data = conn.recv(1024)
                data = data.decode()
                self.recv(data, addr)
            conn.close()
        except:
            print(user + ' Connection lose')
            # 把離開聊天室的從user list中移除
            self.delUsers(conn, addr)
            conn.close()

    # 刪除user
    def delUsers(self, conn, addr):
        a = 0
        for i in users:
            if i[0] == conn:
                users.pop(a)
                print(' Remaining online users: ',
                      end='')
                d = onlines()
                self.recv(d, addr)
                # print出剩下的使用者
                print(d)
                break
            a += 1

    # 把ip, data, addr儲存在queue中
    def recv(self, data, addr):
        lock.acquire()
        try:
            queue.put((addr, data))
        finally:
            lock.release()

    # 把queue中的消息發給所有使用者
    def sendData(self):
        while True:
            if not queue.empty():
                data = ''
                # 拿出queue中的第一個東西
                message = queue.get()
                # 若訊息是string
                if isinstance(message[1], str):
                    for i in range(len(users)):
                        # user[i][1]是使用者名稱, users[i][2]是addr
                        for j in range(len(users)):
                            # 看訊息是從哪個使用者發出來的
                            if message[0] == users[j][2]:
                                print(
                                    ' this: message is from user[{}]'.format(j))
                                data = ' ' + users[j][1] + '：' + message[1]
                                break
                        users[i][0].send(data.encode())
                # data = data.split(':;')[0]
                if isinstance(message[1], list):  # 同上
                    # 如果是list直接發送
                    data = json.dumps(message[1])
                    for i in range(len(users)):
                        try:
                            users[i][0].send(data.encode())
                        except:
                            pass

    def run(self):

        self.s.bind(self.ADDR)
        self.s.listen(5)
        print('Chat server starts running...')
        q = threading.Thread(target=self.sendData)
        q.start()
        while True:
            conn, addr = self.s.accept()
            t = threading.Thread(target=self.tcp_connect, args=(conn, addr))
            t.start()
        self.s.close()


if __name__ == '__main__':
    cserver = ChatServer(PORT)
    cserver.start()

    while True:
        time.sleep(1)
        if not cserver.is_alive():
            print("Chat connection lost...")
            sys.exit(0)
