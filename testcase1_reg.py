import Main.ChatApplication as ca
#--------------initial-----------------
chat_system = ca.initial_chat_controller()
#--------------initial-----------------
#สมัครสมาชิกปกติ
#กรอกข้อมูลครบถ้วน
print("1."+chat_system.register_user("Naphat",'123456789'))
#กรอกข้อมูลไม่ครบ
print("2."+chat_system.register_user('Paramad',''))
#กรอกข้อมูลครบ username ซ้ำ
print("3."+chat_system.register_user('Isaac','1234'))