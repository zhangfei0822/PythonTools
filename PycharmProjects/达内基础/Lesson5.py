# conding:utf-8
import random

all_choice = ['stone', 'knif', 'cloth']
win_list = [['stone', 'knif'], ['knif', 'cloth'], ['cloth', 'stone']]

computer = random.choice(all_choice)
player = input('Please set one choice(石头、剪刀、布)')
print('your choice is: %s, and computer choise is: %s' %(player, computer))
if [player, computer] in win_list:
    print('you win')
elif computer == player:
    print('equal')
else:
    print('you lost')