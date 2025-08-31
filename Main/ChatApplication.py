from datetime import datetime
import random
import string
class Chat_Controller:
    user_id_counter = 0
    noti_id_counter = 0
    room_id_counter = 0
    def __init__(self):
        self.user_list = {}
        self.room_list = []
        self.room_code_map = {}  # room_code -> Chatroom
        self.friends_graph = {}  # user_id → set(friend_ids) เก็บเพื่อนแบบ Undirected Graph
        self.pending_requests = {} # user_id → set(requester_ids) เก็บคำขอเพื่อนที่ยังไม่ได้ตอบ
        self.username_list_fname = {chr(i): {} for i in range(ord('a'), ord('z') + 1)}
    def check_first_char(self,username):
        first_char = username[0].lower()
        if first_char in self.username_list_fname:
            return [first_char,True]
        return [first_char,False]
    def Login(self,username,password):
        f_name,check = self.check_first_char(username)
        if not check:
            return "Error : Please fill Correct Username."
        bucket = self.username_list_fname.get(f_name, {})

        username_id_inbucket = bucket.get(username)
        if not username_id_inbucket:
             return "Error : Username not found,Please Register before login."
        
        user_ins = self.user_list[username_id_inbucket]
        if user_ins.get_password() != password:
            return "Error : Idenify Fail Please fill Correct Password."
        return user_ins.get_id()
    def register_user(self,username_in,password_in):
        if not username_in  or not password_in :
            return "Error : Please fill Username and Passworkd again. "
        f_name,check = self.check_first_char(username_in)
        if not check:
            return f"Error: Username '{username_in}' must start with a letter."
            #เช็คว้า username ซ้ำไม
        bucket = self.username_list_fname[f_name]
        if username_in in bucket:
            return f"Error: Username '{username_in}' is already taken."
        new_user_id = 'user_'+str(self.user_id_counter)
        new_user = User(new_user_id,username_in,password_in)
        self.user_list[new_user_id] = new_user
        bucket[username_in] = new_user_id
        self.user_id_counter += 1 
        return f"Registration successful for user: {username_in}"
    def send_friend_request(self,from_user_id,to_user_id):
        if from_user_id == to_user_id:
            return "Error : Cannot add yourself."
        friends_set = self.friends_graph.get(from_user_id,set())
        if to_user_id in friends_set:
            return "Error : Already freinds."
        pending_set = self.pending_requests.get(to_user_id,set())
        if from_user_id in pending_set:
            return "Error : Friend request already sent."
        
        self.pending_requests.setdefault(to_user_id,set()).add(from_user_id)
        self.create_notification('FR',to_user_id,None,None,from_user_id)
        return f"Friend request sent from {self.search_user_by_user_id(from_user_id).get_username()} to {self.search_user_by_user_id(to_user_id).get_username()}"
    def accept_friend_quest(self,user_id,requester_id):
        pending_set = self.pending_requests.get(user_id,set())
        if requester_id not in pending_set:
            return "Error: No pending request from this user."
        # ลบคำขอจาก pending
        pending_set.remove(requester_id)
         # เพิ่มเพื่อนใน Graph
        self.friends_graph.setdefault(user_id,set()).add(requester_id)
        self.friends_graph.setdefault(requester_id,set()).add(user_id)

        #สร้าง Notification ให้ผู้ส่งคำขอ
        self.create_notification('AF',user_id,None,None,requester_id)
        return f"{self.search_user_by_user_id(user_id)} and {self.search_user_by_user_id(requester_id)} are now Friend."
        pass
    def show_friends(self,user_id):
        frirend_ids = self.friends_graph.get(user_id,set())
        return [self.user_list[fid].get_username() for fid in frirend_ids]
    def remove_friend(self,user_id,friend_id):
        self.friends_graph.get(user_id,set()).discard(friend_id)
        self.friends_graph.get(friend_id,set()).discard(user_id)
        return f"{self.search_user_by_user_id(user_id).get_username()} and {self.search_user_by_user_id(friend_id).get_username()} are no longer freinds." 
    def create_group_chat(self,creator_id,member_ids):
        room_id = f"room_{self.room_id_counter}"
        self.room_id_counter += 1

        room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        new_room = Chatroom(room_id=room_id,room_type='group',members=[creator_id]+member_ids,room_code=room_code)
        self.room_list.append(new_room)
        if new_room.get_room_code() :
            self.room_code_map[new_room.room_code] = new_room

        for uid in [creator_id]+member_ids:
            self.user_list[uid].add_chat_room_user(new_room)
        return f"Group chat {room_id} created with members:{[self.user_list[uid].get_username() for uid in [creator_id]+member_ids]} | Room Code : [{room_code}]"
    def create_private_chat(self,user1_id,user2_id):
        #check have?
        for room in self.room_list:
            if room.get_room_type() == 'private' and room.get_member() == {user1_id,user2_id}:
                return f"Private chat already exists: {room.get_room_id()}"
        #create
        room_id = f"room_{self.room_id_counter}"
        self.room_id_counter += 1
        new_room = Chatroom(room_id=room_id,room_type='private',members=[user1_id,user2_id])
        self.room_list.append(new_room)
        
        #add member
        self.user_list[user1_id].add_chat_room_user(new_room)
        self.user_list[user2_id].add_chat_room_user(new_room)
        return f"Private chat '{room_id}' created between {self.user_list[user1_id].get_username()} and {self.user_list[user2_id].get_username()}"
    def show_chat_in_user(self,user_id):
        user = self.search_user_by_user_id(user_id)
        return user.get_chat_room()
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
    def search_user_by_username(self,username):
        f_name, _ = self.check_first_char(username)
        bucket = self.username_list_fname.get(f_name, {})
        user_id = bucket.get(username)
        return self.user_list.get(user_id) if user_id else None
    def search_user_by_user_id(self,user_id):
        return self.user_list.get(user_id)
    def search_room_by_room_code(self,room_code):
        return self.room_code_map.get(room_code)
    def search_room_by_room_id(self,room_id):
        for room in self.room_list:
            if room.get_room_id() == room_id:
                return room
        return None
    def remove_chat_from_user(self,user_id,room_id):
        pass
    def join_chatroom(self,room_code,user_id):
        user = self.search_user_by_user_id(user_id)
        room = self.search_room_by_room_code(room_code)
        if not user:
            return "Error : User not found."
        if not room:
            return "Error : Room code not valid."
        if user_id in room.get_member():
            return f"{user.get_username()} is already in this room."
        
        room.add_member(user_id)
        user.add_chat_room_user(room)
        return f"{user.get_username()} joined room '{room.get_room_id()}' with code {room_code}"
    def send_message_in_chatroom(self,room_id,user_id,content):
        room = self.search_room_by_room_id(room_id)
        user = self.search_user_by_user_id(user_id)
        c = room.send_message(user,content)
        return c
    def edit_message_in_chatroom(self,room_id,msg_id,user_id,content_edit):
        room = self.search_room_by_room_id(room_id)
        return room.edit_message(msg_id,user_id,content_edit)
    def delete_message_in_chatroom(self,room_id,msg_id,user_id):
        room = self.search_room_by_room_id(room_id)
        return room.edit_message(msg_id,user_id,'[ลบข้อความแล้ว]')
    def chat_history(self,room_id):
        room = self.search_room_by_room_id(room_id)
        return room.chat_history()

class User:
    def __init__(self,user_id,username,password):
        self.user_id = user_id
        self.username = username 
        self.password = password
        self.chat_room_list = ChatRoomList()
        self.notification_deque = DEqueue()
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
    def get_chat_room(self):
        return self.chat_room_list.printRoom()
    def add_chat_room_user(self,new_room):
        self.chat_room_list.add_room(new_room)
class Message:
    def __init__(self, message_id, sender_id,sender_name, content):
        self.message_id = message_id
        self.sender_id = sender_id
        self.sender_name = sender_name
        self.content = content
        self.time_stamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def get_content(self):
        return self.content
    def set_content(self,content):
        self.content = content
    def set_time(self):
        self.time_stamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def get_time(self):
        return self.time_stamp
    def get_sender_id(self):
        return self.sender_id
    def get_message_id(self):
        return self.message_id
    def get_sender_name(self):
        return self.sender_name
class Chatroom:
    def __init__(self,room_id,room_type, members=None,room_code=None):
        self.room_id = room_id
        self.room_type = room_type
        self.member_list = set(members) if members else set()
        self.messages_head = None
        self.messages_tail = None
        self.messages_map = {} # message_id -> MessageNode
        self.messages_counter = 0
        self.created_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.room_code = room_code
    def get_room_code(self):
        return self.room_code
    def add_member(self,user):
        self.member_list.add(user)
    def remove_member(self,user_id):
        if user_id in self.member_list:
            del self.member_list[user_id]
            return True
        return False
    def send_message(self,sender,content):
        if sender.get_id() not in self.member_list:
            return f"Error : User not in this room"
        message_id = f"{self.room_id}_msg_{self.messages_counter}"
        msg =  Message(message_id=message_id,sender_id=sender.get_id(),sender_name=sender.get_username(), content=content)
        node = Node(msg)
        if not self.messages_head:
            self.messages_head = self.messages_tail = node
        else:
            self.messages_tail.next = node
            node.prev = self.messages_tail
            self.messages_tail = node
        self.messages_map[message_id] = node
        self.messages_counter+=1
        return message_id
    def delete_message(self,message_id,sender_id):
        node = self.messages_map.get(message_id)
        if not node:
            return "Error : Message not found."
        if node.data.get_sender_id() != sender_id:
            return "Error : Cannot delete others messages."
        if node.prev:
            node.prev.next = node.next
        else:
            self.messages_head = node.next
        if node.next :
            node.next.prev = node.prev
        else:
            self.messages_tail = node.prev
        del self.messages_map[message_id]
        return "Message deleted successfully."
    def edit_message(self,message_id,sender_id,new_content):
        node = self.messages_map.get(message_id)
        if not node:
            return f"Error: Message not found"
        if node.data.get_sender_id() != sender_id:
            return f"Error: Cannot edit others messages."
        node.data.set_content(new_content)
        node.data.set_time()
        return "Message edited successfully."
    def chat_history(self):
        res = []
        curr = self.messages_head
        while curr:
            m = curr.data
            res.append({
                'message_id' : m.get_message_id(),
                'sender_id' : m.get_sender_id(),
                'sender_name' : m.get_sender_name(),
                'content': m.get_content(),
                'time' : m.get_time()
            })
            curr = curr.next
        return res
    def get_room_id(self):
        return self.room_id
    def get_room_type(self):
        return self.room_type
    def get_member(self):

        return self.member_list
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
class ChatRoomList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.map = {} # room_id -> node
    def add_room(self,chatroom):
        """เพิ่มห้องใหม่ หรือเลื่อนไปหัวถ้ามีอยู่แล้ว"""
        room_id = chatroom.get_room_id()
        if room_id in self.map:
            node = self.map[room_id]
            self.move_to_head(node)
        else:
            node = Node(chatroom)
            self.map[room_id] = node
            self.insert_head(node)
    def remove_room(self,room_id):
        node = self.map.get(room_id)
        if not node:
            return
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if node == self.head:
            self.head = node.next
        if node == self.tail:
            self.tail = node.prev
        del self.map[room_id]
    def get_room(self,room_id):
        return self.map.get(room_id).data if room_id in self.map else None
    def printRoom(self):
        res = []
        curr = self.head
        while curr:
            res.append(curr.data.get_room_id())
            curr = curr.next
        return res
    def insert_head(self,node):
        node.prev = None
        node.next = self.head
        if self.head : 
            self.head.prev = node
        self.head = node
        if not self.tail:
            self.tail = node
    def move_to_head(self,node):
        if node == self.head:
            return
        if node.prev:
            node.prev.next == node.next
        if node.next:
            node.next.prev = node.prev
        if node == self.tail:
            self.tail = node.prev
        node.prev = None
        node.next = self.head
        self.head.prev  = node
        self.head = node

        
def initial_chat_controller():

    chat_system = Chat_Controller()
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
    {"username": "Isaac", "password": "isaacpass123"},
    {"username": "IPEX", "password": "PEXAD"}
    ]
    for user in mock_users:
        chat_system.register_user(user["username"], user["password"])
    return chat_system