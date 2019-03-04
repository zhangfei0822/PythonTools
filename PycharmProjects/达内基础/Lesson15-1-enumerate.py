# enumerate()
# !/usr/bin/env python
import string
alist = [10, 20, 'bob', 'alice']

for i in range(len(alist)):
    print('%d, %s' %(i, alist[i]))

for item in enumerate(alist):
    print(item)

for ind, elem in enumerate(alist):
    print('%s, %s' %(ind, elem))


def check_input_label(label):
    # first character should be '_' or alphabet
    # other letter should be alphabet or num
    # uppercase is different with lowercase
    first_letter = string.ascii_letters + '_'
    other_chrs = first_letter + string.digits
    result = True
    desc = ''
    if label[0] not in first_letter:
        result = False
        desc = 'Captal Letter is not _ or ascii_letters'
    else:
        for ind, ch in enumerate(label[1:]):
            if ch not in (string.ascii_letters + string.digits):
                result = False
                desc = 'The {} character is invalid: {} '.format(ind + 2, ch)
                break
        else:
            desc = ' OK '

    return [result, desc]


if __name__ == '__main__':
    l = input('input the label:')
    res, descr = check_input_label(l)
    print(descr)