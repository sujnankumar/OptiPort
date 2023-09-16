l=[1,2,3,4]
s=[5,6,7,8]
print([(value1, value2) for index, (value1, value2) in enumerate(zip(l, s))])