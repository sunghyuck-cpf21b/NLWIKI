with open('total.txt', mode='w', encoding='utf-8') as f:
    f.write('안녕')


import sys
print(sys.path)

a = 'abcdefabcdef'
b = a.split('abc')
print(b)
count_bc = a.count('bc')
print(count_bc)


a = 1
while True:
    a += 1
    if a > 8 and a < 15:
        continue
    print(a)
    if a == 20:
        break



q = [1,2,3,4,5]
print(q[2:4])


def test(r):
    if r == 1:
        return '1번에서 컷'
    elif r == 2:
        return '2번에서 컷'
    elif r == 3:
        return '3번에서 컷'
    else:
        return '마지막'

print(test(2))


t = [1,2,3,4,5]
t[0] = 0
print(t)

TT = ['1:30:00 PM']
if 'PM' in TT[0]:
    print(TT)


n = 1
t = n%10
print(t)

