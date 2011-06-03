def myfunc1(arg1, arg2):
    return dict(args=[arg1, arg2])

def myfunc2(name):
    return 'Hello %s' % name

def myfunc3():
    return 'Look ma\', no args!'

def myfunc4(s):
    import hashlib
    return hashlib.md5(s).hexdigest()
