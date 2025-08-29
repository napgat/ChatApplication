import Main.ChatApplication as ca
#--------------initial-----------------
chat_system = ca.initial_chat_system()
#--------------initial-----------------
#เข้าสู่ระบบแล้วต้องได้ ins user กลับมา
#เข้าสู่ระบบปกติ
print(chat_system.Login('Naphat','123456789'))
#เข้าสู่ระบบหากมีข้อมูลรหัสผ่านพลาด
print(chat_system.Login('Naphat','123341251'))
#เข้าสูระบบหากชื่อผู้ใชผิดพลาด
print(chat_system.Login('Naat','123456789'))
#เข้าสู่ระบบหากชื่ผู้ใช้ใส่ตัวอักษรพิเศษ
print(chat_system.Login(' Nahpat','123456789'))
