from django import forms
from .models import Comment
# 正常的前端表单代码应该是和本文开头所提及的那样的 HTML 代码，但是我们目前并没有写这些代码，
# 而是写了一个 CommentForm 这个 Python 类。
# 通过调用这个类的一些方法和属性，django 将自动为我们创建常规的表单代码

class CommentForm(forms.ModelForm):#表单类必须继承自forms.Form类或者forms.ModelForm类
    class Meta:
        model=Comment#表明这个表单对应的数据库模型是Comment类
        fields=['name','email','url','text']#制定了表单需要显示的字段
