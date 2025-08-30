import time
class Chat_system:
    user_id = 0
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
            new_user_id = 'user_'+str(self.user_id)
            new_user = User(new_user_id,username_in,password_in)
            self.user_list[new_user_id] = new_user
            self.username_list_fname[f_name].append(new_user_id)
            self.user_id += 1 
            return f"Registration successful for user: {username_in}"
        else:
            return f"Error: Username '{username_in}' must start with a letter."
    def send_friend_request(self):
        pass
    def accept_friend_quest(self):
        pass
    def create_group_chat(self):
        pass
    def show_notification(self):
        pass
class User:
    def __init__(self,user_id,username,password):
        self.user_id = user_id
        self.username = username 
        self.password = password
        self.friend_list = []
        self.chat_room_list = []
        self.notication_list = []
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
    def __init__(self):
        self.noti_id = None
        self.title = None
        self.context_noti = None
        self.time_stamp = None
        self.isRead = False
class FriendRequest:
    def __init__(self):
        self.sender_id = None
        self.to_member_id = None
        self.is_accept = False

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