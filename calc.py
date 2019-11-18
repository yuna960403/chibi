
def calc(s):
    print('s=',s)
    nums1 = map(int,s.split('+'))
    nums2 = map(int,s.split('*'))
    print('nums=',nums1)
    return sum(nums1)

print(calc("1+2+3"))
print(calc("1+2*3"))

#途中（次回やるnums2から）
