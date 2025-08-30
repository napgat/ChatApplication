from datetime import datetime
class Chat_system:
    user_id_counter = 0
    noti_id_counter = 0
    def __init__(self):
        self.user_list = {}
        self.room_list = []
        self.username_list_fname = {}
        self.chat_all = []
        for i in range(ord('a'),ord('z') + 1):
            self.username_list_fname[chr(i)] = []
    def check_first_char(self,username):
        first_char = username[0].lower()
        if first_char in self.username_list_fname:
            return [first_char,True]
        return [first_char,False]
    def Login(self,username,password):
        f_name,check = self.check_first_char(username)
        if check:
            for id in self.username_list_fname[f_name]:
                user_ins = self.user_list[id]
                if user_ins.get_username() == username:
                    if user_ins.get_password() == password:
                        return user_ins.get_id()
                    else:
                        return "Error : Idenify Fail Please fill Correct Password."
                else:
                    return "Error : Username not found,Please Register before login."
            return "Error : UnCorrect Username."
        else:
            return "Error : Please fill Correct Username."
    def register_user(self,username_in,password_in):
        if username_in == '' or password_in == '':
            return "Error : Please fill Username and Passworkd again. "
        f_name,check = self.check_first_char(username_in)
        if check:
            #เช็คว้า username ซ้ำไม
            if len(self.username_list_fname[f_name]) > 0:
                for id in self.username_list_fname[f_name]:
                    user_ins = self.user_list[id]
                    if user_ins.get_username() == username_in:
                        return f"Error: Username '{username_in}' is already taken."
            new_user_id = 'user_'+str(self.user_id_counter)
            new_user = User(new_user_id,username_in,password_in)
            self.user_list[new_user_id] = new_user
            self.username_list_fname[f_name].append(new_user_id)
            self.user_id_counter += 1 
            return f"Registration successful for user: {username_in}"
        else:
            return f"Error: Username '{username_in}' must start with a letter."
    def send_friend_request(self):
        pass
    def accept_friend_quest(self):
        pass
    def create_group_chat(self):
        pass
    def show_notification(self,user_id):
        data_output = []
        data_init = {}
        noti_ins_deque = self.user_list[user_id].show_notification()
        for noti in noti_ins_deque:
            data_init['type'] = noti.get_noti_type()
            data_init['title'] =  noti.get_title()
            data_init['content'] = noti.get_content()
            data_init['date_time'] = noti.get_time()
            data_output.append(data_init)
            data_init = {}
        return data_output
    def Logout(self):
        return None
    def create_notification(self,notif_type,user_id,title,message,requester_id=None):
        if notif_type == 'SYS':
            if user_id == None:
                for user in self.user_list.values():
                    id_inifi = 'ini_'+ str(self.noti_id_counter)
                    noti_ins = SystemNotification(id_inifi,user.get_id(),title,message)
                    user.add_notifcation(noti_ins)
            else:
                id_inifi = 'ini_'+ str(self.noti_id_counter)
                noti_ins = SystemNotification(id_inifi,self.user_list[user_id].get_id(),title,message)
                self.user_list[user_id].add_notifcation(noti_ins)
        elif notif_type == "FR":
            if requester_id == None:
                return "Error NO Requester"
            else:
                id_inifi = 'int_' + str(self.noti_id_counter)
                title = "Request Add Friend From : " + self.user_list[requester_id].get_username()
                message = 'You received a friend request from ' + self.user_list[requester_id].get_username() + " check [FRIEND] now."
                noti_ins = FriendRequestNotification(id_inifi,user_id,requester_id,title,message,False)
                self.user_list[user_id].add_notifcation(noti_ins)
        elif notif_type == 'AF':
            id_inifi = 'int_' + str(self.noti_id_counter)
            title = "Friend request has been accepted From " + self.user_list[user_id].get_username()
            message = f"Your friend[{self.user_list[user_id].get_username()}] request has been accepted."
            noti_ins = FriendRequestNotification(id_inifi,requester_id,user_id,title,message,True)
            self.user_list[requester_id].add_notifcation(noti_ins)
        self.noti_id_counter +=1
    def search_user_by_user_id(self,user_id):
        return self.user_list[user_id]  
class User:
    def __init__(self,user_id,username,password):
        self.user_id = user_id
        self.username = username 
        self.password = password
        self.friend_list = []
        self.chat_room_list = []
        self.notification_deque = DEqueue()
    def send_friend_request(self):
        pass
    def accept_friend_request(self):
        pass
    def remove_friend(self):
        pass
    def show_notication(self):
        pass
    def get_all_friend(self):
        return self.friend_list
    def get_username(self):
        return self.username
    def get_password(self):
        return self.password
    def get_id(self):
        return self.user_id
    def add_notifcation(self,notification):
        self.notification_deque.insert_head(notification)
    def show_notification(self):
        return self.notification_deque.printList()
class Message:
    def __init__(self):
        self.message_id = None
        self.sender_id = None
        self.content = None
        self.time_stamp = None
class Chatroom:
    def __init__(self):
        self.room_id = None
        self.member_list = []
        self.messages = None
    def add_member(self):
        pass
    def remove_member(self):
        pass
    def send_message(self):
        pass
    def chat_history(self):
        pass
class Notification:
    def __init__(self,noti_id,title,user_id,content,noti_type):
        self.noti_id = noti_id
        self.title = title
        self.content = content
        self.user_id = user_id
        self.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.isRead = False
        self.noti_type = noti_type
        self.color = ''
    def get_noti_id(self):
        return self.noti_id
    def get_noti_type(self):
        return self.noti_type
    def get_title(self):
        return self.title
    def get_content(self):
        return self.content
    def get_time(self):
        return self.timestamp
class FriendRequestNotification(Notification):
    def __init__(self,noti_id,user_id,requester_id,title,content,status):
        super().__init__(noti_id,title,user_id,content,'FR' if status == False else "FA")
        self.requester_id = requester_id
        self.is_accepted = status
class SystemNotification(Notification):
    def __init__(self,noti_id,user_id,title,content):
        super().__init__(noti_id,title,user_id,content,'SYS')
class FriendRequest:
    def __init__(self):
        self.sender_id = None
        self.to_member_id = None
        self.is_accept = False
class Node:
    def __init__(self,data):
        self.data = data
        self.prev = None
        self.next = None
class DEqueue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    def insert_head(self,data):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1
    def insert_tail(self,data):
        new_node = Node(data)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1
    def pop_head(self):
        if not self.head:
            return None
        node = self.head
        self.head = node.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self.size -= 1
        return node.data
    def pop_tail(self):
        if not self.tail:
            return None
        node = self.tail
        self.tail = node.prev
        if self.tail:
            self.tail.next = None
        else:
            self.head = None
        self.size -= 1
        return node.data
    def __len__(self):
        return self.size
    def printList(self):
        res = []
        current = self.head
        while current:
            res.append(current.data)
            current = current.next
        return res            

def initial_chat_system():
    chat_system = Chat_system()
    mock_users = [
    {"username": "Alice", "password": "alice1234"},
    {"username": "Naphat", "password": "123456789"},
    {"username": "Alex", "password": "alex1234"},
    {"username": "Bob", "password": "bob5678"},
    {"username": "Charlie", "password": "charlie001"},
    {"username": "David", "password": "davidpass"},
    {"username": "Eva", "password": "evapass2025"},
    {"username": "Frank", "password": "frank12345"},
    {"username": "Grace", "password": "gracepassword"},
    {"username": "Hannah", "password": "hannah2023"},
    {"username": "Isaac", "password": "isaacpass123"}
    ]
    for user in mock_users:
        chat_system.register_user(user["username"], user["password"])
    return chat_system