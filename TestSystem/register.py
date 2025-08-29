import ChatApplication as ca
user_id = 0
user_list = {}
username_first_name = {}
for i in range(ord('a'),ord('z') + 1):
    username_first_name[chr(i)] = []

def check_first_char(username):
    first_char = username[0].lower()
    if first_char in username_first_name:
        return [first_char,True]
    return [first_char,False]
def register_user(username_in,password_in):
        f_name,check = check_first_char(username_in)
        if check:
            #เช็คว้า username ซ้ำไม
            if len(username_first_name[f_name]) > 1:
                for id in username_first_name[f_name]:
                    user_ins = user_list[id]
                    if user_ins.get_username() == user_ins:
                        return f"Username '{username_in}' is already taken."
            new_user = ca.User(username_in,password_in)
            new_user_id = 'user_'+str(user_id)
            user_list[new_user_id] = new_user
            username_first_name[f_name].append(new_user_id)
            user_id += 1 
            return f"Registration successful for user: {username_in}"
        else:
            return f"Error: Username '{username_in}' must start with a letter."

#สมัครสมาชิก
#กรอกข้อมูล
#ถ้าสมัครได้
print(register_user('Naphat','123456789'))
