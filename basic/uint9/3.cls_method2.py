class Student:  #Student为类的名称（类名）由一个或多个单词组成，每个单词的首字母大写，其余小写
   native_pace='吉林'  #直接写在类里的变量，称为类属性
   def __init__(self,name,age):
       self.name=name    #self.name 称为实体属性  ，进行了 一个赋值的操作，将局部变量的name的值赋给实体属性
       self.age=age

   #实例方法
   def eat(self):
       print('学生在吃饭...')

    #静态方法
   @staticmethod
   def method():
       print('我使用了statticmethod进行修饰，所以我是静态方法')

    #类方法
   @classmethod
   def cm(cls):
       print('我是类方法，因为我使用了classmethod进行修饰')
#在类之外定义的称为函数，在类之内定义的称为方法
def drink():
    print('喝水')

#创建Student类的对象
stu1=Student('张三',20)
print(id(stu1))
print(type(stu1))
print(stu1)
print('---------------------')
print(id(Student))  #Student是类的名称
print(type(Student))
print(Student)