import Main.ChatApplication as ca
import time
#--------------initial-----------------
chat_system = ca.initial_chat_system()
#เมื่อผู้ใช้ Login เข้ามาแล้ว
user_id_login = chat_system.Login('Naphat','123456789')
#--------------initial-----------------
#ให้ระบบส่งการแจ้งเตือนถึง user ทุกคน#
chat_system.create_notification(notif_type='SYS',user_id=None,title='Test Message',message='This is Test Message')
time.sleep(5)
chat_system.create_notification(notif_type='SYS',user_id=None,title='Test Message2',message='This is Test Message2222')
#กดปุ่มแสดงการแจ้งเตือน
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