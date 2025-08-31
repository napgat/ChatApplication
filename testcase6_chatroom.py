import Main.ChatApplication as ca
#--------------initial-----------------
chat_system = ca.initial_chat_controller()
#เมื่อผู้ใช้ Login เข้ามาแล้ว
user_id_login = chat_system.Login('Naphat','123456789')
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
code = input()
print(chat_system.join_chatroom(room_code=code,user_id='user_5'))
print(chat_system.show_chat_in_user('user_5'))