import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import tkinter.simpledialog as simpledialog  # ใส่ไว้ด้านบนร่วมกับ import อื่น ๆ
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
        self.create_notification(notif_type='SYS',user_id=from_user_id,title='Friend Request Pending',message=f'You have sent a friend request to {self.search_user_by_user_id(to_user_id).get_username()}')
        self.create_notification('FR',to_user_id,None,None,from_user_id)

        return f"Friend request sent from {self.search_user_by_user_id(from_user_id).get_username()} to {self.search_user_by_user_id(to_user_id).get_username()}"
    def accept_friend_quest(self,user_id,requester_id):
        #user_id ผู้รับ
        #requester ผู้ส่ง
        pending_set = self.pending_requests.get(user_id,set())
        if requester_id not in pending_set:
            return "Error: No pending request from this user."
        # ลบคำขอจาก pending
        pending_set.remove(requester_id)
         # เพิ่มเพื่อนใน Graph
        self.friends_graph.setdefault(user_id,set()).add(requester_id)
        self.friends_graph.setdefault(requester_id,set()).add(user_id)

        self.create_notification(notif_type='SYS',user_id=user_id,title='Friend Request Accepted',message=f'You have accepted {self.search_user_by_user_id(requester_id).get_username()}  friend request successfully')
        #สร้าง Notification ให้ผู้ส่งคำขอ
        self.create_notification('AF',user_id,None,None,requester_id)
        
        return f"{self.search_user_by_user_id(user_id)} and {self.search_user_by_user_id(requester_id)} are now Friend."
    def show_friends(self,user_id):
        frirend_ids = self.friends_graph.get(user_id,set())
        return [self.user_list[fid].get_username() for fid in frirend_ids]
    def remove_friend(self,user_id,friend_id):
        self.friends_graph.get(user_id,set()).discard(friend_id)
        self.friends_graph.get(friend_id,set()).discard(user_id)
        print(user_id)
        self.create_notification(notif_type='SYS',user_id=user_id,title='Friend Removed',message=f'You have removed {self.search_user_by_user_id(friend_id).get_username()}  from your friends list')
        return f"{self.search_user_by_user_id(user_id).get_username()} and {self.search_user_by_user_id(friend_id).get_username()} are no longer freinds." 
    def create_group_chat(self,creator_id,member_ids):
        # เช็คว่า member_ids มีสมาชิกซ้ำหรือไม่
        if not creator_id:
            return "Error: Login first"
        if creator_id in member_ids:
            return "Error: Creator cannot be a member of the group."
        if len(member_ids) != len(set(member_ids)):
            return "Error: Duplicate member found in the list."
        for member_id in member_ids:
            if not self.is_friend(creator_id, member_id):
                return f"Error: {self.user_list[creator_id].get_username()} is not friends with {self.user_list[member_id].get_username()}."
        room_id = f"room_{self.room_id_counter}"
        self.room_id_counter += 1
        room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        new_room = Chatroom(room_id=room_id,room_type='group',members=[creator_id]+member_ids,room_code=room_code)
        self.room_list.append(new_room)
        if new_room.get_room_code() :
            self.room_code_map[new_room.get_room_code()] = new_room

        for uid in [creator_id]+member_ids:
            self.user_list[uid].add_chat_room_user(new_room)
        return f"Group chat {room_id} created with members:{[self.user_list[uid].get_username() for uid in [creator_id]+member_ids]} | Room Code : [{room_code}]"
    def create_private_chat(self,user1_id,user2_id):
        if not user1_id:
            return "Error: Login First"
        if user1_id == user2_id:
            return "You cannot create a private chat with your own name."
        if self.is_friend(user1_id,user2_id):
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
        return "You cannot create a private chat with this person because you are not friends yet or wrong username."
    def show_chat_in_user(self,user_id):
        user = self.search_user_by_user_id(user_id)
        return user.get_chat_room()
    def is_friend(self, user_id, other_user_id):
    # เช็คว่า user_id เป็นเพื่อนกับ other_user_id หรือไม่
        friends_set = self.friends_graph.get(user_id, set())
        if other_user_id in friends_set:
            return True
        return False
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
    def get_chatroom_members(self, room_id):
        # ค้นหาห้องแชทตาม room_id
        room = self.search_room_by_room_id(room_id)
        if not room:
            return "Error: Room not found."
        
        # คืนค่ารายชื่อสมาชิกในห้องแชท
        return [(uid, self.user_list[uid].get_username()) for uid in room.get_member()]
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
        if not user_id:
            return "Error : Login First"
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
        #  return room.delete_message(msg_id, user_id)
        return room.edit_message(msg_id,user_id,'[ลบข้อความแล้ว]')
    def chat_history(self,room_id):
        room = self.search_room_by_room_id(room_id)
        return room.chat_history()
    def remove_member_from_chatroom(self, room_id, user_id, operator_id):
        # ค้นหาห้องแชทตาม room_id
        room = self.search_room_by_room_id(room_id)
        if not room:
            return "Error: Room not found."
        
        # เช็คว่าผู้ใช้คือสมาชิกในห้องนี้หรือไม่
        if user_id not in room.get_member():
            return f"Error: {self.user_list[user_id].get_username()} is not a member of this room."
        
        # ลบสมาชิกออกจากห้องแชท
        room.remove_member(user_id)
        self.user_list[user_id].remove_chat_room_user(room)
        
        # สร้างข้อความแจ้งให้ผู้ดำเนินการทราบ
        operator_name = self.user_list[operator_id].get_username()
        removed_user_name = self.user_list[user_id].get_username()
        return f"{operator_name} has removed {removed_user_name} from room {room.get_room_id()}"

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
    def remove_chat_room_user(self, room):
        """ ลบสมาชิกออกจากห้องแชทในรายการห้องแชทของผู้ใช้ """
        self.chat_room_list.remove_room(room.get_room_id())
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
        # self.room_title = room_title
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
        # if user_id in self.member_list:
        #     del self.member_list[user_id]
        #     return True
        # return False
        before = len(self.member_list)
        self.member_list.discard(user_id)
        return len(self.member_list) != before    
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
        # if node == self.head:
        #     return
        # if node.prev:
        #     node.prev.next == node.next
        # if node.next:
        #     node.next.prev = node.prev
        # if node == self.tail:
        #     self.tail = node.prev
        # node.prev = None
        # node.next = self.head
        # self.head.prev  = node
        # self.head = node
        if node == self.head:
            return
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if node == self.tail:
            self.tail = node.prev
        node.prev = None
        node.next = self.head
        if self.head:
            self.head.prev = node
        self.head = node
        if not self.tail:
            self.tail = node

        
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


# ---------- Utilities ----------
def beautify_style(root):
    root.title("Chat Application — Tkinter UI")
    root.geometry("1100x720")
    root.minsize(1000, 650)

    style = ttk.Style()
    # ใช้ธีม 'clam' เพื่อรองรับการปรับสีได้ดี
    try:
        style.theme_use("clam")
    except:
        pass

    style.configure("TNotebook.Tab", padding=(16, 8), font=("Segoe UI", 10, "bold"))
    style.configure("Card.TFrame", background="#1f2937")  # slate-800
    style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))
    style.configure("SubHeader.TLabel", font=("Segoe UI", 12, "bold"))
    style.configure("Muted.TLabel", foreground="#6b7280")  # gray-500
    style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=8)
    style.configure("Good.TLabel", foreground="#10b981")  # emerald-500
    style.configure("Warn.TLabel", foreground="#ef4444")  # red-500
    style.configure("Hint.TLabel", foreground="#93c5fd")  # blue-300

    # ปุ่มหลัก
    style.configure("Primary.TButton", padding=8, font=("Segoe UI", 10, "bold"))
    style.map("Primary.TButton",
              background=[("active", "#2563eb")],
              foreground=[("active", "white")])

    # กรอบการ์ดโค้งมน
    style.configure("Card.TLabelframe", background="#111827", foreground="#e5e7eb", padding=12)
    style.configure("Card.TLabelframe.Label", font=("Segoe UI", 10, "bold"))

def divider(parent):
    f = ttk.Separator(parent, orient="horizontal")
    f.pack(fill="x", pady=8)
    return f


# ---------- แอปหลัก ----------
class ChatApp(tk.Tk):
    def __init__(self, controller_factory):
        super().__init__()
        beautify_style(self)

        # สร้างระบบ + แพตช์
        self.controller = controller_factory()

        self.current_user_id = None
        self.current_username = None
        self.current_room_id = None

        # Root layout
        container = ttk.Frame(self, padding=12)
        container.pack(fill="both", expand=True)

        header = ttk.Label(container, text="Chat Application", style="Header.TLabel")
        header.pack(anchor="w")

        

        ttk.Label(container, text="A simple yet sleek Tkinter UI for your Chat_Controller backend.",
                  style="Muted.TLabel").pack(anchor="w", pady=(0, 10))

        divider(container)
        # แถบหัวสำหรับแสดงสถานะล็อกอิน (ขวาบน)
        self.header_bar = ttk.Frame(container)
        self.header_bar.pack(fill="x", pady=(0, 10))

        self.login_status = ttk.Label(self.header_bar, text="", style="Good.TLabel")
        self.login_status.pack(side="right")

        self.logout_btn = ttk.Button(self.header_bar, text="Logout", command=self.do_logout)
        self.logout_btn.pack(side="right", padx=8)
        self.logout_btn.pack_forget()  # ยังไม่ล็อกอิน ให้ซ่อนปุ่มไว้ก่อน

        self.tabs = ttk.Notebook(container)
        self.tabs.pack(fill="both", expand=True)

        # Tabs
        self.login_tab = ttk.Frame(self.tabs, padding=10)
        self.home_tab = ttk.Frame(self.tabs, padding=10)
        self.rooms_tab = ttk.Frame(self.tabs, padding=10)
        self.chat_tab = ttk.Frame(self.tabs, padding=10)
        self.noti_tab = ttk.Frame(self.tabs, padding=10)

        self.tabs.add(self.login_tab, text="Login / Register")
        self.tabs.add(self.home_tab, text="Friends")
        self.tabs.add(self.rooms_tab, text="Rooms")
        self.tabs.add(self.chat_tab, text="Chat")
        self.tabs.add(self.noti_tab, text="Notifications")

        # Build each tab UIs
        self.build_login_tab()
        self.build_home_tab()
        self.build_rooms_tab()
        self.build_chat_tab()
        self.build_noti_tab()
        # ตั้งค่าเริ่มต้นให้ป้ายสถานะว่าง
        self.update_login_badge()

        # Prefill mock
        # (หากต้องการเริ่มระบบจาก initial_chat_controller ของคุณ ให้ส่งเข้ามาจาก controller_factory)
        # ที่นี่เราทำผ่าน factory แล้ว

    def update_login_badge(self):
        """อัปเดตป้ายสถานะผู้ใช้มุมขวาบน: แสดงชื่อเมื่อมีผู้ใช้ล็อกอิน, ว่างเมื่อยังไม่ล็อกอิน"""
        if self.current_user_id:
            self.login_status.config(
                text=f"Signed in as: {self.current_username}  ({self.current_user_id})"
            )
            # แสดงปุ่ม Logout
            try:
                self.logout_btn.pack_info()
            except tk.TclError:
                # ถ้ายังไม่เคย pack ให้ pack ใหม่
                self.logout_btn.pack(side="right", padx=8)
        else:
            self.login_status.config(text="")
            # ซ่อนปุ่ม Logout
            self.logout_btn.pack_forget()
        # ====== Chat helpers / state ======
    def _build_scrollable_chat(self, parent):
        """สร้างพื้นที่แสดงบับเบิลแบบเลื่อนขึ้นลงได้"""
        wrapper = ttk.Frame(parent)
        wrapper.pack(fill="both", expand=True)

        
        self.chat_canvas = tk.Canvas(wrapper, highlightthickness=0)
        vsb = ttk.Scrollbar(wrapper, orient="vertical", command=self.chat_canvas.yview)
        self.chat_canvas.configure(yscrollcommand=vsb.set)

        self.chat_inner = tk.Frame(self.chat_canvas, bg="#0b1220")  # พื้นหลังโทนเข้มดูสบายตา
        self.chat_window = self.chat_canvas.create_window((0, 0), window=self.chat_inner, anchor="nw")

        self.chat_canvas.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # ปรับ scrollregion ตามขนาดเนื้อหาภายใน
        def _on_configure(e):
            self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
            # ทำให้ความกว้างภายในยืดเท่ากับ canvas เพื่อให้ anchor e/w ชิดจริง
            self.chat_canvas.itemconfigure(self.chat_window, width=self.chat_canvas.winfo_width())

        self.chat_inner.bind("<Configure>", _on_configure)
        self.chat_canvas.bind("<Configure>", _on_configure)

    def _render_chat_bubbles(self, messages):
        """วาดบับเบิลใหม่ทั้งหมดตาม messages"""
        # ล้างของเดิม
        for w in self.chat_inner.winfo_children():
            w.destroy()
        self.selected_msg_id = None
        self.bubble_map = {}  # msg_id -> bubble_frame

        # สไตล์บับเบิล
        ME_BG = "#1d4ed8"      # น้ำเงิน (เรา)
        ME_FG = "white"
        OTHER_BG = "#111827"   # เทาเข้ม (คนอื่น)
        OTHER_FG = "#e5e7eb"

        for m in messages:
            is_me = (m["sender_id"] == self.current_user_id)

            # แถวหนึ่งของบับเบิล (ใช้ Frame + pack anchor ซ้าย/ขวา)
            row = tk.Frame(self.chat_inner, bg="#0b1220")
            row.pack(fill="x", expand=True, pady=4, padx=8)

            # คอนเทนเนอร์ของบับเบิล (เพื่อให้ขอบ/เลือกได้)
            bubble = tk.Frame(row, bg=ME_BG if is_me else OTHER_BG)
            meta = tk.Label(bubble,
                            text=f'{m["sender_name"]} • {m["time"]}',
                            fg="#cbd5e1", bg=bubble["bg"],
                            font=("Segoe UI", 8, "italic"))
            text = tk.Label(bubble,
                            text=m["content"],
                            wraplength=520,
                            justify="left",
                            fg=ME_FG if is_me else OTHER_FG,
                            bg=bubble["bg"],
                            font=("Segoe UI", 10))
            meta.pack(anchor="w", padx=10, pady=(8, 0))
            text.pack(anchor="w", padx=10, pady=(2, 8))

            # ขอบมนดูเป็นบับเบิล
            bubble.configure(highlightthickness=0, bd=0)
            bubble.pack(pady=0)

            # จัดชิดซ้าย/ขวา
            if is_me:
                bubble.pack(anchor="e", padx=(120, 0))  # เว้นด้านซ้ายเยอะเพื่อให้ชิดขวา
            else:
                bubble.pack(anchor="w", padx=(0, 120))  # เว้นด้านขวาเยอะเพื่อให้ชิดซ้าย

            # ให้คลิกเลือกได้ เฉพาะของเราเท่านั้นที่จะ "เลือก" แล้วลบได้
            def _on_click(evt, msg_id=m["message_id"], mine=is_me, bf=bubble):
                self._on_bubble_click(msg_id, mine, bf)
            # bind ที่ทั้งกรอบและ label ข้างใน
            for bind_target in (bubble, meta, text):
                bind_target.bind("<Button-1>", _on_click)

            # เก็บ map
            self.bubble_map[m["message_id"]] = bubble

        # เลื่อนไปล่างสุด
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)

    def _clear_bubble_selection(self):
        # เอากรอบ selection ออก
        if getattr(self, "selected_msg_id", None) and self.selected_msg_id in self.bubble_map:
            bf = self.bubble_map[self.selected_msg_id]
            bf.configure(highlightthickness=0, highlightbackground=bf["bg"])
        self.selected_msg_id = None

    def _on_bubble_click(self, msg_id, is_mine, bubble_frame):
        """คลิกบับเบิล: เลือกเฉพาะของเรา และโชว์กรอบเส้น"""
        # ล้างของเดิม
        self._clear_bubble_selection()
        if not is_mine:
            # ของคนอื่น เลือกไม่ได้
            return
        self.selected_msg_id = msg_id
        bubble_frame.configure(highlightthickness=2, highlightbackground="#f59e0b")  # amber เส้นเน้น

    def do_logout(self):
        """ล้างสถานะเมื่อออกจากระบบ และเคลียร์หน้าจอบางส่วน"""
        self.current_user_id = None
        self.current_username = None
        self.current_room_id = None

        # เคลียร์ตาราง/รายการต่าง ๆ
        for tree in [
            getattr(self, "pending_tree", None),
            getattr(self, "friends_tree", None),
            getattr(self, "rooms_tree", None),
            getattr(self, "rooms_small", None),
            getattr(self, "msg_tree", None),
            getattr(self, "noti_tree", None),
        ]:
            if tree is not None:
                tree.delete(*tree.get_children())

        # รีเซ็ต label ห้องแชท
        if hasattr(self, "chat_room_lbl"):
            self.chat_room_lbl.config(text="Room: -")

        # อัปเดตป้ายสถานะและพากลับไปแท็บ Login
        self.update_login_badge()
        self.tabs.select(self.login_tab)
        messagebox.showinfo("Logout", "ออกจากระบบแล้ว")

    # ---------- Login/Register ----------
    def build_login_tab(self):
        f = self.login_tab

        # Card: Login
        login_card = ttk.Labelframe(f, text="Login", style="Card.TLabelframe")
        login_card.pack(side="left", fill="both", expand=True, padx=(0, 6))

        ttk.Label(login_card, text="Username").pack(anchor="w", pady=(4, 2))
        self.login_user_var = tk.StringVar()
        ttk.Entry(login_card, textvariable=self.login_user_var).pack(fill="x")

        ttk.Label(login_card, text="Password").pack(anchor="w", pady=(8, 2))
        self.login_pass_var = tk.StringVar()
        ttk.Entry(login_card, textvariable=self.login_pass_var, show="*").pack(fill="x")

        ttk.Button(login_card, text="Login", style="Primary.TButton",
                   command=self.do_login).pack(anchor="e", pady=12)

        # Card: Register
        reg_card = ttk.Labelframe(f, text="Register", style="Card.TLabelframe")
        reg_card.pack(side="left", fill="both", expand=True, padx=(6, 0))

        ttk.Label(reg_card, text="Username").pack(anchor="w", pady=(4, 2))
        self.reg_user_var = tk.StringVar()
        ttk.Entry(reg_card, textvariable=self.reg_user_var).pack(fill="x")

        ttk.Label(reg_card, text="Password").pack(anchor="w", pady=(8, 2))
        self.reg_pass_var = tk.StringVar()
        ttk.Entry(reg_card, textvariable=self.reg_pass_var, show="*").pack(fill="x")

        ttk.Button(reg_card, text="Register", style="Primary.TButton",
                   command=self.do_register).pack(anchor="e", pady=12)

        # Info
        ttk.Label(f, text="Tip: ระบบมี mock users ไว้แล้ว (Alice, Alex, Bob, ...). ลองสมัครผู้ใช้ใหม่ของคุณเองได้เลย.",
                  style="Hint.TLabel").pack(anchor="w", pady=(10, 0))

    def do_login(self):
        u = self.login_user_var.get().strip()
        p = self.login_pass_var.get().strip()
        if not u or not p:
            messagebox.showwarning("Warning", "กรุณากรอก Username/Password")
            return
        res = self.controller.Login(u, p)
        if isinstance(res, str) and res.startswith("Error"):
            messagebox.showerror("Login Failed", res)
        else:
            self.current_user_id = res
            self.current_username = self.controller.search_user_by_user_id(res).get_username()
            messagebox.showinfo("Login", f"ยินดีต้อนรับ {self.current_username}")
            self.refresh_friends()
            self.refresh_requests()
            self.refresh_my_rooms()
            self.refresh_chat_history()
            self.refresh_notifications()
            self.update_login_badge()
            self.tabs.select(self.home_tab)

    def do_register(self):
        u = self.reg_user_var.get().strip()
        p = self.reg_pass_var.get().strip()
        res = self.controller.register_user(u, p)
        if isinstance(res, str) and res.startswith("Error"):
            messagebox.showerror("Register Failed", res)
        else:
            messagebox.showinfo("Register", res)

    # ---------- Friends tab ----------
    def build_home_tab(self):
        f = self.home_tab

        left = ttk.Labelframe(f, text="Find / Add Friend", style="Card.TLabelframe")
        left.pack(side="left", fill="both", expand=True, padx=(0, 6))

        ttk.Label(left, text="Search username").pack(anchor="w")
        self.search_user_var = tk.StringVar()
        ttk.Entry(left, textvariable=self.search_user_var).pack(fill="x", pady=(2, 6))

        ttk.Button(left, text="Send Friend Request", style="Primary.TButton",
                   command=self.send_friend_request).pack(anchor="e")

        divider(left)

        ttk.Label(left, text="Pending Requests (to me)", style="SubHeader.TLabel").pack(anchor="w", pady=(6, 4))
        self.pending_tree = ttk.Treeview(left, columns=("uid", "name"), show="headings", height=8)
        self.pending_tree.heading("uid", text="User ID")
        self.pending_tree.heading("name", text="Username")
        self.pending_tree.pack(fill="both", expand=True)
        ttk.Button(left, text="Accept Selected Request", command=self.accept_selected_request).pack(anchor="e", pady=8)

        # Right
        right = ttk.Labelframe(f, text="My Friends", style="Card.TLabelframe")
        right.pack(side="left", fill="both", expand=True, padx=(6, 0))

        self.friends_tree = ttk.Treeview(right, columns=("uid", "name"), show="headings", height=14)
        self.friends_tree.heading("uid", text="User ID")
        self.friends_tree.heading("name", text="Username")
        self.friends_tree.pack(fill="both", expand=True)

        ttk.Button(right, text="Remove Selected Friend", command=self.remove_selected_friend).pack(anchor="e", pady=8)

    def send_friend_request(self):
        if not self.current_user_id:
            messagebox.showwarning("Login required", "กรุณา Login ก่อน")
            return
        name = self.search_user_var.get().strip()
        if not name:
            messagebox.showwarning("Input", "กรุณากรอก Username")
            return
        user = self.controller.search_user_by_username(name)
        if not user:
            messagebox.showerror("Not found", "ไม่พบผู้ใช้นี้")
            return
        res = self.controller.send_friend_request(self.current_user_id, user.get_id())
        if isinstance(res, str) and res.startswith("Error"):
            messagebox.showerror("Friend Request", res)
        else:
            messagebox.showinfo("Friend Request", res)
            self.refresh_notifications()

    def refresh_requests(self):
        # ดึงจาก pending_requests ของฉัน
        self.pending_tree.delete(*self.pending_tree.get_children())
        if not self.current_user_id:
            return
        pending = self.controller.pending_requests.get(self.current_user_id, set())
        for uid in pending:
            uname = self.controller.user_list[uid].get_username()
            self.pending_tree.insert("", "end", values=(uid, uname))

    def accept_selected_request(self):
        sel = self.pending_tree.selection()
        if not sel:
            messagebox.showinfo("Select", "กรุณาเลือกคำขอเพื่อน")
            return
        item = self.pending_tree.item(sel[0])
        requester_id = item["values"][0]
        res = self.controller.accept_friend_quest(self.current_user_id, requester_id)
        if isinstance(res, str) and res.startswith("Error"):
            messagebox.showerror("Accept Fail", res)
        else:
            messagebox.showinfo("Accept", "ยืนยันเป็นเพื่อนเรียบร้อย")
        self.refresh_requests()
        self.refresh_friends()
        self.refresh_notifications()

    def refresh_friends(self):
        self.friends_tree.delete(*self.friends_tree.get_children())
        if not self.current_user_id:
            return
        friend_ids = self.controller.friends_graph.get(self.current_user_id, set())
        for fid in friend_ids:
            uname = self.controller.user_list[fid].get_username()
            self.friends_tree.insert("", "end", values=(fid, uname))

    def remove_selected_friend(self):
        sel = self.friends_tree.selection()
        if not sel:
            messagebox.showinfo("Select", "กรุณาเลือกเพื่อน")
            return
        fid = self.friends_tree.item(sel[0])["values"][0]
        res = self.controller.remove_friend(self.current_user_id, fid)
        messagebox.showinfo("Remove Friend", res)
        self.refresh_friends()
        self.refresh_notifications()

    # ---------- Rooms tab ----------
    def build_rooms_tab(self):
        f = self.rooms_tab

        # Left: My Rooms / Join by code
        left = ttk.Labelframe(f, text="My Rooms / Join", style="Card.TLabelframe")
        left.pack(side="left", fill="both", expand=True, padx=(0, 6))

        ttk.Label(left, text="My Rooms", style="SubHeader.TLabel").pack(anchor="w")
        self.rooms_tree = ttk.Treeview(left, columns=("room_id",), show="headings", height=14)
        self.rooms_tree.heading("room_id", text="Room ID")
        self.rooms_tree.pack(fill="both", expand=True)

        btns = ttk.Frame(left)
        btns.pack(fill="x", pady=6)
        ttk.Button(btns, text="Open Room", command=self.open_selected_room).pack(side="right")

        divider(left)
        ttk.Label(left, text="Join by Room Code", style="SubHeader.TLabel").pack(anchor="w", pady=(4, 2))

        code_frame = ttk.Frame(left)
        code_frame.pack(fill="x")
        ttk.Label(code_frame, text="Code").pack(side="left")
        self.join_code_var = tk.StringVar()
        ttk.Entry(code_frame, textvariable=self.join_code_var, width=14).pack(side="left", padx=6)
        ttk.Button(code_frame, text="Join", style="Primary.TButton",
                   command=self.join_by_code).pack(side="left")

        # Right: Create rooms
        right = ttk.Labelframe(f, text="Create Room", style="Card.TLabelframe")
        right.pack(side="left", fill="both", expand=True, padx=(6, 0))

        # Private
        ttk.Label(right, text="Create Private Chat", style="SubHeader.TLabel").pack(anchor="w", pady=(0, 2))
        self.private_with_var = tk.StringVar()
        p_row = ttk.Frame(right); p_row.pack(fill="x", pady=2)
        ttk.Label(p_row, text="Friend username").pack(side="left")
        ttk.Entry(p_row, textvariable=self.private_with_var).pack(side="left", padx=6)
        ttk.Button(p_row, text="Create", command=self.create_private_chat).pack(side="left")

        divider(right)

        # Group
        ttk.Label(right, text="Create Group Chat", style="SubHeader.TLabel").pack(anchor="w", pady=(0, 2))
        ttk.Label(right, text="กรอก username (เพื่อน) คั่นด้วยเครื่องหมายจุลภาค ,",
                  style="Muted.TLabel").pack(anchor="w")

        self.group_members_var = tk.StringVar()
        g_row = ttk.Frame(right); g_row.pack(fill="x", pady=2)
        ttk.Entry(g_row, textvariable=self.group_members_var).pack(side="left", fill="x", expand=True)
        ttk.Button(g_row, text="Create Group", style="Primary.TButton",
                   command=self.create_group_chat).pack(side="left", padx=6)

        self.group_result_lbl = ttk.Label(right, text="", style="Good.TLabel")
        self.group_result_lbl.pack(anchor="w", pady=6)

    def refresh_my_rooms(self):
        self.rooms_tree.delete(*self.rooms_tree.get_children())
        if not self.current_user_id:
            return
        room_ids = self.controller.show_chat_in_user(self.current_user_id) or []
        for rid in room_ids:
            self.rooms_tree.insert("", "end", values=(rid,))

    def join_by_code(self):
        code = self.join_code_var.get().strip().upper()
        if not code:
            messagebox.showwarning("Input", "กรุณากรอก Room Code")
            return
        res = self.controller.join_chatroom(code, self.current_user_id)
        if isinstance(res, str) and res.startswith("Error"):
            messagebox.showerror("Join", res)
        else:
            messagebox.showinfo("Join", res)
            self.refresh_my_rooms()

    def create_private_chat(self):
        name = self.private_with_var.get().strip()
        if not name:
            messagebox.showwarning("Input", "กรุณากรอกชื่อเพื่อน")
            return
        user = self.controller.search_user_by_username(name)
        if not user:
            messagebox.showerror("Not found", "ไม่พบผู้ใช้นี้")
            return
        res = self.controller.create_private_chat(self.current_user_id, user.get_id())
        messagebox.showinfo("Create Private", res)
        self.refresh_my_rooms()

    def create_group_chat(self):
        if not self.current_user_id:
            messagebox.showerror("Error", "กรุณนาเข้าสู่ระบบเพื่อดำเนินการต่อ")
            return
        names = [x.strip() for x in self.group_members_var.get().split(",") if x.strip()]
        if not names:
            messagebox.showwarning("Input", "กรุณากรอกชื่อเพื่อนอย่างน้อย 1 คน")
            return
        member_ids = []
        for n in names:
            u = self.controller.search_user_by_username(n)
            if not u:
                messagebox.showerror("Not found", f"ไม่พบผู้ใช้: {n}")
                return
            member_ids.append(u.get_id())
        res = self.controller.create_group_chat(self.current_user_id, member_ids)
        if isinstance(res, str) and res.startswith("Error"):
            messagebox.showerror("Create Group", res)
        else:
            # self.group_result_lbl.config(text=res)
            #ต้องเป็นแจ้งเตือน
            self.refresh_my_rooms()

    def open_selected_room(self):
        sel = self.rooms_tree.selection()
        if not sel:
            messagebox.showinfo("Select", "กรุณาเลือกห้อง")
            return
        rid = self.rooms_tree.item(sel[0])["values"][0]
        self.current_room_id = rid
        self.refresh_chat_history()
        self.tabs.select(self.chat_tab)

    # ---------- Chat tab ----------
    def build_chat_tab(self):
        f = self.chat_tab

        top = ttk.Frame(f)
        top.pack(fill="x")
        self.chat_room_lbl = ttk.Label(top, text="Room: -", style="SubHeader.TLabel")
        self.chat_room_lbl.pack(side="left")

        divider(f)

        # --- Bottom: แถบส่งข้อความ ปักไว้ล่างสุดของแท็บ ---
        bottom = ttk.Frame(f)
        bottom.pack(side="bottom", fill="x", pady=6)   # <-- สำคัญ: side="bottom"
        self.msg_var = tk.StringVar()
        ttk.Entry(bottom, textvariable=self.msg_var).pack(side="left", fill="x", expand=True, padx=(0, 6))
        ttk.Button(bottom, text="Send", style="Primary.TButton", command=self.send_message).pack(side="left")
        ttk.Button(bottom, text="Delete Selected (mine)", command=self.delete_selected_message).pack(side="left", padx=6)

        # --- Body: เอาไว้เหนือ bottom เติมพื้นที่ที่เหลือทั้งหมด ---
        body = ttk.Frame(f)
        body.pack(side="top", fill="both", expand=True)  # <-- ย้ายมาอยู่บน และให้ expand

        # Left: My Rooms
        left = ttk.Labelframe(body, text="My Rooms", style="Card.TLabelframe")
        left.pack(side="left", fill="y", padx=(0, 6))

        self.rooms_small = ttk.Treeview(left, columns=("room_id",), show="headings", height=20)
        self.rooms_small.heading("room_id", text="Room ID")
        self.rooms_small.pack(fill="y", expand=False)
        ttk.Button(left, text="Open", command=self.open_room_from_small).pack(pady=6)

        # Center: Chat bubbles
        center = ttk.Labelframe(body, text="Chat", style="Card.TLabelframe")
        center.pack(side="left", fill="both", expand=True)

        self._build_scrollable_chat(center)

        # state
        self.selected_msg_id = None
        self.bubble_map = {}


    def open_room_from_small(self):
        sel = self.rooms_small.selection()
        if not sel:
            messagebox.showinfo("Select", "กรุณาเลือกห้อง")
            return
        rid = self.rooms_small.item(sel[0])["values"][0]
        self.current_room_id = rid
        self.refresh_chat_history()

    def refresh_chat_history(self):
        # refresh room lists
        self.rooms_small.delete(*self.rooms_small.get_children())
        for rid in (self.controller.show_chat_in_user(self.current_user_id) or []):
            self.rooms_small.insert("", "end", values=(rid,))
        # set label
        self.chat_room_lbl.config(text=f"Room: {self.current_room_id or '-'}")

        if not self.current_room_id:
            # ถ้ายังไม่เลือกห้อง ล้างหน้าจอ
            self._render_chat_bubbles([])
            return

        msgs = self.controller.chat_history(self.current_room_id) or []
        self._render_chat_bubbles(msgs)

    def send_message(self):
        text = self.msg_var.get().strip()
        if not text:
            return
        if not self.current_room_id:
            messagebox.showwarning("Room", "ยังไม่ได้เลือกห้อง")
            return
        res = self.controller.send_message_in_chatroom(self.current_room_id, self.current_user_id, text)
        if isinstance(res, str) and res.startswith("Error"):
            messagebox.showerror("Send", res)
        else:
            self.msg_var.set("")
            self.refresh_chat_history()

    def edit_selected_message(self):
        if not self.current_room_id:
            messagebox.showwarning("Room", "ยังไม่ได้เลือกห้อง")
            return
        if not self.selected_msg_id:
            messagebox.showinfo("Select", "กรุณาคลิกเลือกข้อความของคุณก่อน")
            return
        # ขอข้อความใหม่
        old = ""
        msgs = self.controller.chat_history(self.current_room_id) or []
        for m in msgs:
            if m["message_id"] == self.selected_msg_id:
                old = m["content"]
                break
        new = simpledialog.askstring("Edit message", "แก้ไขข้อความ:", initialvalue=old, parent=self)
        if new is None:
            return
        res = self.controller.edit_message_in_chatroom(self.current_room_id,
                                                    self.selected_msg_id,
                                                    self.current_user_id,
                                                    new)
        if isinstance(res, str) and res.startswith("Error"):
            messagebox.showerror("Edit", res)
        else:
            self.refresh_chat_history()

    def delete_selected_message(self):
        if not self.current_room_id:
            messagebox.showwarning("Room", "ยังไม่ได้เลือกห้อง")
            return
        if not self.selected_msg_id:
            messagebox.showinfo("Select", "กรุณาคลิกเลือกข้อความของคุณก่อน")
            return
        # ลบทิ้ง (ฝั่ง backend ทำเป็น edit เป็น '[ลบข้อความแล้ว]' ตามโค้ดของคุณ)
        res = self.controller.delete_message_in_chatroom(self.current_room_id,
                                                         self.selected_msg_id,
                                                         self.current_user_id)
        if isinstance(res, str) and res.startswith("Error"):
            messagebox.showerror("Delete", res)
        else:
            self.refresh_chat_history()

    # ---------- Notifications tab ----------
    def build_noti_tab(self):
        f = self.noti_tab

        ttk.Label(f, text="Notifications", style="SubHeader.TLabel").pack(anchor="w")
        self.noti_tree = ttk.Treeview(f, columns=("type", "title", "content", "time"), show="headings", height=20)
        self.noti_tree.heading("type", text="Type")
        self.noti_tree.heading("title", text="Title")
        self.noti_tree.heading("content", text="Content")
        self.noti_tree.heading("time", text="Time")
        self.noti_tree.column("type", width=80)
        self.noti_tree.column("title", width=220)
        self.noti_tree.column("content", width=500)
        self.noti_tree.column("time", width=150)
        self.noti_tree.pack(fill="both", expand=True, pady=(6, 0))

        ttk.Button(f, text="Refresh", command=self.refresh_notifications).pack(anchor="e", pady=8)

    def refresh_notifications(self):
        self.noti_tree.delete(*self.noti_tree.get_children())
        if not self.current_user_id:
            return
        data = self.controller.show_notification(self.current_user_id) or []
        print(data)
        for n in data:
            self.noti_tree.insert("", "end", values=(n["type"], n["title"], n["content"], n["date_time"]))


# ---------- main ----------
def controller_factory():
    # ใช้ initial_chat_controller ของคุณเพื่อมี mock users พร้อมใช้
    return initial_chat_controller()

if __name__ == "__main__":
    app = ChatApp(controller_factory)
    app.mainloop()