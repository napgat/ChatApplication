import time
class Chat_system:
    user_id = 0
    def __init__(self):
        self.user_list = {}
        self.room_list = []
        self.username_first_name = {}
        self.chat_all = []
        for i in range(ord('a'),ord('z') + 1):
            self.username_first_name[chr(i)] = []
    def check_first_char(self,username):
        first_char = username[0].lower()
        if first_char in self.username_first_name:
            return [first_char,True]
        return [first_char,False]
    def Login(self):
        pass
    def register_user(self,username_in,password_in):
        f_name,check = self.check_first_char(username_in)
        if check:
            #เช็คว้า username ซ้ำไม
            if len(self.username_first_name[f_name]) > 1:
                for id in self.username_first_name[f_name]:
                    user_ins = self.user_list[id]
                    if user_ins.get_username() == user_ins:
                        return f"Username '{username_in}' is already taken."
            new_user = User(username_in,password_in)
            new_user_id = 'user_'+str(self.user_id)
            self.user_list[new_user_id] = new_user
            self.username_first_name[f_name].append(new_user_id)
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
    def __init__(self,username,password):
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
    def get_username(self):
        return self.username
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

chat_system = Chat_system()


#แสดงรายการชื่อตัวแรก

chat_system.register_user("user1", "pass")
chat_system.register_user("user2", "pass")
print(chat_system.user_list)
print(chat_system.username_first_name)