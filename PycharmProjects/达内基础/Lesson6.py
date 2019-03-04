# while1.py
# encoding = utf-8

"""
counter = 1
sum = 0
while counter <= 100:
    sum += counter
    counter += 1
print(sum)
"""

# while2.py
import random

all_choice = ['stone', 'knif', 'cloth']
win_list = [['stone', 'knif'], ['knif', 'cloth'], ['cloth', 'stone']]

prompt = """(1) stone
(2) knife
(3) cloth
Please input your choice : """
pwin = 0
cwin = 0
while pwin < 2 and cwin < 2:
    computer = random.choice(all_choice)
    player = input(prompt)

    print('your choice is: %s, and computer choise is: %s' %(player, computer))
    if [player, computer] in win_list:
        print('you win')
        pwin += 1
    elif computer == player:
        print('equal')
    else:
        print('you lost')
        cwin += 1

if cwin == 2:
    print('finally, you win')
else:
    print('you lost!')


# while3.py
# 1-100 sum
sum100 = 0
counter = 0
while counter < 100:
    counter += 1
    # if counter % 2 == 1:
    if counter % 2:
        continue
    sum100 += counter
print(sum100)