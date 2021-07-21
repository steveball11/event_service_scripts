#%%
def fun(a, *args, **kwargs):
    print("a={}".format(a))
    for arg in args:
        print('Optional argument: {}'.format( arg ) )
    print(kwargs.keys())
    for k, v in kwargs.items():
        print('Optional kwargs argument key: {} value {}'.format(k, v))

fun(1,22,33,c=22,Interact={"Interact":"123456","a":"100"},k2=110)
# %%

def define_rules(**info):
    return info
define_rules(a=10)

# %%

def fun1(a,b,*args, **kwargs):
    print(kwargs)
    if "d" in kwargs:
        print(kwargs["d"])
    a + b
    return a+b


fun1(10,11,c=100,d=1000)
# %%
class Base(object):
    def __init__(self, *args, data=None, **kwargs):
        print('data is: ', data)

class MyBaseObject(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MyObject(MyBaseObject):
    def __init__(self, *args, game=None, **kwargs):
        super().__init__(*args, **kwargs)
        print('game is: ', game)

my_data = {'game': 'UT', 'data': '3d'}
print(1,MyBaseObject(**my_data))
print(2,MyObject(**my_data))
# %%

def print_func_name(func):
    def warp(*args, **kwargs):
        print("Now use function '{}'".format(func.__name__))
        func(*args, **kwargs)
    return warp


@print_func_name
def dog_bark(x):
    print("Bark !!!",x+1)

if __name__ == "__main__":
    dog_bark(x=20)


# %%
# 汽車類別
class Cars:
    pass
# 摩托車類別
class Motorcycle:
    pass
# 建立Cars類別的物件
mazda = Cars()  # 建立Cars類別的物件
mazda.color = "blue"  #顏色屬性
mazda.seat = 4  #座位屬性
print(isinstance(mazda, Cars))  # 執行結果：True
print(isinstance(mazda, Motorcycle))  # 執行結果：False
print(mazda.color)
# %%
class Chicken(object):
    weight = 1.1 #類別屬性

    def __init__(self):
        self.age = 18 #實例屬性(or 資料屬性)

    def get_age(self):
        return self.age
c = Chicken()
# %%
class Chicken():
    weight = 1.1 #類別屬性

    def __init__(self):
        self.age = 18 #實例屬性(or 資料屬性)

    def get_age(self):
        return self.age
c = Chicken()
# %%
