a = [str(i) for i in range(5)]
print(';'.join(a))
print(a)
print(str(a))

from datetime import datetime
t = datetime(2011,11,11)
print(t)
print('2011-11-11 00:00:00')
T = '2011-11-11 00:00:00'
T = datetime.strptime(T, "%Y-%m-%d %H:%M:%S")
print(type(T))