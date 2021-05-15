from django.shortcuts import render,get_object_or_404
from django.template import loader
# Create your views here.
from django.http import HttpResponse
# from .models import Question
from django.http import Http404
from .models import Post,Category,Tag
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
import re


# 从模板文件夹下加载模板文件并将一个字典对象传入视图
def index(request):
    post_list=Post.objects.all().order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

def blogs(request):
    post_list=Post.objects.all().order_by('-created_time')
    return render(request,'blog/blogs.html',{'post_list':post_list})

def about(request):
    return render(request,'blog/about.html')

def contact(request):
    return render(request,'blog/contact.html')

def detail(request,pk):
    post=get_object_or_404(Post,pk=pk)
    md=markdown.Markdown(extensions=['markdown.extensions.extra',
    'markdown.extensions.codehilite',#语法高亮扩展
    TocExtension(slugify=slugify),#允许自动生成目录
    ])
    # 在渲染 Markdown 文本时加入了 toc 拓展后，就可以在文中插入目录了。方法是在书写 Markdown 文本时，
    # 在你想生成目录的地方插入 [TOC] 标记即可。
    post.text_body=md.convert(post.text_body)#md中会自动生成toc摘要
    m=re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>',md.toc,re.S)
    post.toc=m.group(1) if m is not None else ''#在post文章中自动生成了摘要
    return render(request,'blog/details.html',context={'post':post})

def archive(request,year,month):
    post_list=Post.objects.filter(created_time__year=year,
    created_time__month=month).order_by('-created_time')
    print('测试'+post_list)
    return render(request,'blog/index.html',context={'post_list':post_list})

def category(request,pk):
    cate=get_object_or_404(Category,pk=pk)#pk是分类的id
    post_list=Post.objects.filter(category=cate).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

def tag(request,pk):
    t=get_object_or_404(Tag,pk=pk)
    post_list=Post.objects.filter(tags=t).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})