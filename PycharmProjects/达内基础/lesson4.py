# encoding=utf-8
# import getpass
# username = input('username: ')
# # password = input('password:')
# password = getpass.getpass('password: ')
# if username == 'bob' and password == '123456':
#     print('Login successful')
# else:
#     print('Login incorrect')
'''
logic:
just like a film

'''

# grade2
score = int(input('Score:'))
if score >= 60 and score < 70:
    print('D')
elif 70 <= score < 80:
    print('C')
elif 80 <= score < 90:
    print('B')
elif 90 <= score <= 100:
    print('A')
else:
    print('you need more effert ! ')