import Main.ChatApplication as ca
import time
#--------------initial-----------------
chat_system = ca.initial_chat_controller()
#เมื่อผู้ใช้ Login เข้ามาแล้ว
user_id_login = chat_system.Login('Naphat','123456789')
#--------------initial-----------------
#ให้ระบบส่งการแจ้งเตือนถึง user ทุกคน#
# chat_system.create_notification(notif_type='SYS',user_id=None,title='Test Message',message='This is Test Message')
# time.sleep(1)
# chat_system.create_notification(notif_type='SYS',user_id=None,title='Test Message2',message='This is Test Message2222')
# #ให้ระบบส่งการแจ้งเตือนถึงบางคน
# chat_system.create_notification(notif_type='SYS',user_id=user_id_login,title='New Register',message='Welcome To ChatApplication..')

#เมื่อ user_2 เพิ่มเพื่อนไอดีนี้
chat_system.create_notification(notif_type='FR',user_id=user_id_login,title=None,message=None,requester_id='user_2')
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

#เมื่อ userนี้ตอบรับ เพิ่มเพื่อนไอดีนี้
chat_system.create_notification(notif_type='AF',user_id=user_id_login,title=None,message=None,requester_id='user_2')
#กดปุ่มแสดงการแจ้งเตือน

output = chat_system.show_notification('user_2')
#แสดงการแจ้งเตือน
for noti in output:
    print("-----------------------------------")
    print(f"""
    ({noti['type']})Title : {noti['title']}
    {noti['content']}
    Date:{noti['date_time']}
    """)
    print("-----------------------------------")