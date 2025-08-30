import Main.ChatApplication as ca
#--------------initial-----------------
chat_system = ca.initial_chat_system()
#เมื่อผู้ใช้ Login เข้ามาแล้ว
user_id_login = chat_system.Login('Naphat','123456789')
#--------------initial-----------------
#ระบบเพื่อน
#ค้นหาเพื่อนตาม username
print(chat_system.search_user_by_username('Alex'))
#แสดงชื่อเพื่อน และ ปุ่มกดเพิ่ม
user_id_to_add = chat_system.search_user_by_username('Alex').get_id()
print(chat_system.send_friend_request(user_id_login,user_id_to_add))
#Alex ดูการแจ้งเตือน
user_id_login_2 = chat_system.Login('Alex','alex1234')
print(user_id_login_2)

#กดปุ่มแสดงการแจ้งเตือน
output = chat_system.show_notification(user_id_login_2)
#แสดงการแจ้งเตือน
for noti in output:
    print("-----------------------------------")
    print(f"""
    ({noti['type']})Title : {noti['title']}
    {noti['content']}
    Date:{noti['date_time']}
    """)
    print("-----------------------------------")
#กดยอมรับเพื่อน
print(chat_system.accept_friend_quest(user_id_login_2,user_id_login))

#Naphat กดปุ่มแสดงการแจ้งเตือน

output = chat_system.show_notification(user_id_login)
#แสดงการแจ้งเตือน
for noti in output:
    print("-----------------------------------")
    print(f"""
    ({noti['type']})Title : {noti['title']}
    {noti['content']}
    Date:{noti['date_time']}
    """)
    print("-----------------------------------")

#Naphat กดแสดงชื่อเพื่อน
print(chat_system.show_friends(user_id_login))
#Alex กดแสดงชื่อเพื่อน
print(chat_system.show_friends(user_id_login_2))

#Naphat กดยกเลิกเพื่อน Alex
print(chat_system.remove_friend(user_id_login,user_id_login_2))
#Naphat กดแสดงชื่อเพื่อนอีกครั้ง
print(chat_system.show_friends(user_id_login))
#Alex กดแสดงชื่อเพื่อน
print(chat_system.show_friends(user_id_login_2))



