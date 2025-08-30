import Main.ChatApplication as ca
#--------------initial-----------------
chat_system = ca.initial_chat_system()
#เข้าสู่ระบบแล้วต้องได้ ins user กลับมา
#เข้าสู่ระบบปกติ
user_id_login = chat_system.Login('Naphat','123456789')
#--------------initial-----------------
user_id_login = chat_system.Logout()
print(user_id_login)