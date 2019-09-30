
def calc(s):
    print('@',s)
    nums = s.split('+')
    print('nums=',nums)
    return int(s)

print(calc("1+2"))
