import cPickle as p

shop_list = ['apple', 'banana', 'pear', 'peach']

f = open('data.txt', 'w')

p.dump(shop_list, f)

f.close()


f = open('data.txt')

myList = p.load(f)

f.close()

print(myList)
