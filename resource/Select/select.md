python 选择语句
一.条件选择语句

　　Python中条件选择语句的关键字为：if 、elif 、else这三个。其基本形式如下：

复制代码
if condition:
    block
elif condition:
    block
...
else:
    block
	
其中elif和else语句块是可选的。对于if和elif只有condition为True时，该分支语句才执行，只有当if和所有的elif的condition都为False时，才执行else分支。注意Python中条件选择语句和C中的区别，C语言中condition必须要用括号括起来，在Python中不用，但是要注意condition后面有个冒号。

 　　下面这个是成绩划分等级的一个例子：
 score=input()
if score<60:
    print "D"
elif score<80:
    print "C"
elif score<90:
    print "B"
else:
    print "A"