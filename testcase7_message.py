import Main.ChatApplication as ca
#--------------initial-----------------
chat_system = ca.initial_chat_controller()
#เมื่อผู้ใช้ Login เข้ามาแล้ว
user_id_login = chat_system.Login('Naphat','123456789')
#สร้างห้องส่วนตัว
print(chat_system.create_private_chat(user_id_login,'user_2'))
print(chat_system.show_chat_in_user(user_id_login))
#--------------initial-----------------
#ส่งข้อความล่าสุด 
print(chat_system.send_message_in_chatroom('room_0',user_id_login,'สวัสดีค้าบ'))
#ส่งข้อความล่าสุด 
print(chat_system.send_message_in_chatroom('room_0','user_2','สวัสดีจ้า'))
#แสดงประวัติห้องแชท
output = chat_system.chat_history('room_0')
print("---------------------------------------")
for msg in output:
    print(f'{msg['message_id']}:[{msg['time']}] {msg['sender_name']} : {msg['content']}')
print("---------------------------------------")

#ส่งข้อความล่าสุด 
print(chat_system.edit_message_in_chatroom('room_0','room_0_msg_1','user_2','สวัสดีเจ้า'))

#แสดงประวัติห้องแชท
output = chat_system.chat_history('room_0')
print("---------------------------------------")
for msg in output:
    print(f'{msg['message_id']}:[{msg['time']}] {msg['sender_name']} : {msg['content']}')
print("---------------------------------------")

#ลบข้อความ Naphat msgแรก 
print(chat_system.delete_message_in_chatroom('room_0','room_0_msg_0',user_id_login))
#ส่งข้อความล่าสุด 
print(chat_system.send_message_in_chatroom('room_0',user_id_login,'ขอโทษเมื่อพิมพ์ผิด'))

#แสดงประวัติห้องแชท
output = chat_system.chat_history('room_0')
print("---------------------------------------")
for msg in output:
    print(f'{msg['message_id']}:[{msg['time']}] {msg['sender_name']} : {msg['content']}')
print("---------------------------------------")
