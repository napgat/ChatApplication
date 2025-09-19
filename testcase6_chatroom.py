import Main.ChatApplication as ca
#--------------initial-----------------
chat_system = ca.initial_chat_controller()
#เมื่อผู้ใช้ Login เข้ามาแล้ว
user_id_login = chat_system.Login('Naphat','123456789')
#เพิ่มเพื่อนให้เรียบร้อยก่อน
#Alex กับ Naphat
chat_system.friends_graph.setdefault(user_id_login,set()).add('user_2')
chat_system.friends_graph.setdefault('user_2',set()).add(user_id_login)
#Naphat กับ user_3 กับ User_4
chat_system.friends_graph.setdefault(user_id_login,set()).add('user_3')
chat_system.friends_graph.setdefault('user_3',set()).add(user_id_login)

chat_system.friends_graph.setdefault(user_id_login,set()).add('user_4')
chat_system.friends_graph.setdefault('user_4',set()).add(user_id_login)
#--------------initial-----------------
#สร้างห้องส่วนตัว
print(chat_system.create_private_chat(user_id_login,'user_2'))

print(chat_system.show_chat_in_user(user_id_login))

#เมื่อผู้ใช้Alex Login เข้ามาแล้ว
user_id_login_2 = chat_system.Login('Alex','alex1234')
#สร้างห้องส่วนตัวกับ Naphat ต้องสร้างไม่ได้
print(chat_system.create_private_chat(user_id_login_2,user_id_login))
#สร้างห้องGroup
print(chat_system.create_group_chat(user_id_login,['user_2','user_3','user_4']))
#เข้าร่วมห้องโดยใช้ Room code
# code = input()
# print(chat_system.join_chatroom(room_code=code,user_id='user_5'))
# print(chat_system.show_chat_in_user('user_5'))

#สร้างห้องด้วยชื่อตัวเอง 
# print(chat_system.create_private_chat(user_id_login,user_id_login))

#ยังไม่เป็นเพื่อน ก็สร้างห้องได้ ทั้งสองชนิดเลย | เช็คว่า คนสร้าง นั้นเพื่อนทุกคนไหม
#private /
# print(chat_system.create_private_chat(user_id_login,'iserr'))
#group /

#แจ้งเตือนว่ามีห้องถูกสร้าง

#สร้างห้องโดยไม่มี user_id ได้เฉย
#private /
# print(chat_system.create_private_chat(None,'user_2'))
#Group 
# print(chat_system.create_group_chat(None,['user_2','user_3','user_4']))

#Join ห้องต้องมี user_id ของคนที่จะ join ด้วย /

#Join ห้องมีที่ตัวเองมีแล้วได้ไหม /

#ดูสมาชิกให้ห้องแชทได้ไหม
print(chat_system.get_chatroom_members('room_1'))


#ลบสมาชิกในห้องแชทได้ไหม
print(chat_system.remove_member_from_chatroom('room_1','user_2',user_id_login))

print(chat_system.get_chatroom_members('room_1'))