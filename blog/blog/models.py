from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#对应的数据库表


#每一个模型类都是django.db.models.Model的子类，
# 而模型的每一个属性都是Field类的实例，表示一个数据库表的字段。
# 每个Field类实例变量的名字都是数据库字段名（例如question_text和pub_date），
# 因此在给字段起名字的时候一定要注意是否适合数据库。为了满足不同数据库的需要，
# Django提供了几十个Field子类，不同的Field类在实例化的时候会接收不同的参数
class Category(models.Model):
    name=models.CharField(max_length=100)

class Tag(models.Model):
    name=models.CharField(max_length=100)

#文章类
class Post(models.Model):
    #文章标题
    text_title=models.CharField(max_length=70)
    text_body=models.TextField()#文章内容
    created_time=models.DateTimeField()#文章创建时间
    modified_time=models.DateTimeField()#上一次文章修改时间
    text_abstract=models.CharField(max_length=200,blank=True)#摘要允许为空

    #一篇文章只能对应一个分类，但是可以对应多个标签，一个分类下可以有多个标签
    # 数据被删除时，被关联的数据的行为，我们这里假定当某个分类被删除时，该分类下全部文章也同时被删除，因此     # 使用 models.CASCADE 参数，意为级联删除。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 
    # ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    tags=models.ManyToManyField(Tag,blank=True)

     # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 
    # django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 
    # Category 类似。
    author=models.ForeignKey(User,on_delete=models.CASCADE)
