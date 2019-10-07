class Counter(object):
    __slots__ = ['cnt']     #なくてもいい

    def __init__(self):
        self.cnt = 0

    def count(self):
        self.cnt += 1

    def doublecount(self):
        self.cnt += 2

    def reset(self):
        self.cnt = 0

    def show(self):
        print(self.cnt)

    def __repr__(self):     #文字列を返すと表示される
        return str(self.cnt)

c = Counter()
c.show()
c.doublecount()
c.show()
print(type(c))
print(c)