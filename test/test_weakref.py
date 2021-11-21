import sys
import weakref


class A:
    def __init__(self):
        self.i = 1

    def a(self):
        print(self.i)

class B:
    def __init__(self):
        self.obj = None
        self.func = None

    def p(self):

        ref = self.obj
        if ref:
            self.func(self.obj)

    def ref(self, a):
        print(dir(a))
        self.obj = weakref.proxy(a.__self__)
        print(dir(self.obj))
        self.func = a.__func__

a = A()
a.a()
a.__class__.a(a)
print("ref:{}".format(sys.getrefcount(a)))
b = B()
b.ref(a.a)
print("ref:{}".format(sys.getrefcount(a)))
b.p()
print("ref:{}".format(sys.getrefcount(a)))
del a

b.p()
print("ref:{}".format(sys.getrefcount(a)))