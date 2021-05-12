#存放自定义的模板标签代码
from django import template
from ..models import Post,Category,Tag
register=template.Library()#实例化一个template.Library类，并将函数show_recent_posts装饰为register.inclusion_tag,
#这样就告诉django，这个函数是我们自定义的一个类型为inclusion_tag的模板标签

@register.inclusion_tag('blog/inclusions/_recent_posts.html',takes_context=True)
def show_recent_posts(context,num=5):#默认显示5篇最新文章
    return{
        'recent_post_list':Post.objects.all().order_by('-created_time')[:num],
    }

@register.inclusion_tag('blog/inclusions/_archives.html',takes_context=True)
def show_archives(context):
    return {
        'data_list':Post.objects.dates('created_time','month',order='DESC'),
    }

@register.inclusion_tag('blog/inclusions/_categories.html',takes_context=True)
def show_categories(context):
    return {
        'category_list':Category.objects.all(),
    }

@register.inclusion_tag('blog/inclusions/_tags.html',takes_context=True)
def show_tags(context):
    return {
        'tag_list':Tag.objects.all(),
    }