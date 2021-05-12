from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
# Create your models here.
#对应的数据库表


#每一个模型类都是django.db.models.Model的子类，
# 而模型的每一个属性都是Field类的实例，表示一个数据库表的字段。
# 每个Field类实例变量的名字都是数据库字段名（例如question_text和pub_date），
# 因此在给字段起名字的时候一定要注意是否适合数据库。为了满足不同数据库的需要，
# Django提供了几十个Field子类，不同的Field类在实例化的时候会接收不同的参数
class Category(models.Model):
    name=models.CharField(max_length=100)
    class Meta:
        verbose_name='分类'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name
class Tag(models.Model):
    name=models.CharField(max_length=100)
    class Meta:
        verbose_name='标签'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name

#文章类
class Post(models.Model):
    #文章标题
    text_title=models.CharField('标题',max_length=70)
    text_body=models.TextField('正文')#文章内容
    created_time=models.DateTimeField('创建时间',default=timezone.now)#文章创建时间
    modified_time=models.DateTimeField('修改时间')#上一次文章修改时间
    text_abstract=models.CharField('摘要',max_length=200,blank=True)#摘要允许为空

    #一篇文章只能对应一个分类，但是可以对应多个标签，一个分类下可以有多个标签
    # 数据被删除时，被关联的数据的行为，我们这里假定当某个分类被删除时，该分类下全部文章也同时被删除，因此     # 使用 models.CASCADE 参数，意为级联删除。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 
    # ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    category=models.ForeignKey(Category,verbose_name='分类',on_delete=models.CASCADE)
    tags=models.ManyToManyField(Tag,verbose_name='标签',blank=True)

     # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 
    # django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 
    # Category 类似。
    author=models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)

    #配置model的一些特性是通过model的内部类Meta中来定义。
    class Meta:
        verbose_name='文章'#verbose_name来指定对应的model在admin后台的显示名称
        verbose_name_plural=verbose_name#表示多篇文章时的复数显示形式
    def __str__(self):
        return self.text_title

    # 所以这里问题的关键是每次保存模型时，都应该修改 modified_time 的值。
    # 每一个 Model 都有一个 save 方法，这个方法包含了将 model 数据保存到数据库中的逻辑。
    # 通过覆写这个方法，在 model 被 save 到数据库前指定 modified_time 的值为当前时间不就可以了？
    def save(self,*args,**kwargs):
        self.modified_time=timezone.now()
        md=markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        #先将markdown文本渲染成HTML文本
        #strip_tags去掉HTML文本的全部HTML标签
        #从文本摘取前54个字符赋值给abstraction
        if self.text_abstract=='':
            self.text_abstract=strip_tags(md.convert(self.text_body))[:54]

        super().save(*args,**kwargs)

        # truncatechars 过滤器可以截取模板变量值的前 N 个字符显示。
        # {{ post.body|truncatechars:54 }}可以得到同样的效果

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})#reverse函数解析这个detail视图函数对应的url，
        # 如果 Post 的 id（或者 pk，这里 pk 和 id 是等价的） 是 255 的话，
        # 那么 get_absolute_url 函数返回的就是 /posts/255/ ，这样 Post 自己就生成了自己的 URL。
