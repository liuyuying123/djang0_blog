from django.shortcuts import render
from django.contrib import messages

# Create your views here.

from blog.models import Post
from django.shortcuts import get_object_or_404,redirect,render
from django.views.decorators.http import require_POST
from .forms import CommentForm

@require_POST
def comment(request,post_pk):
    #先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来
    post=get_object_or_404(Post,pk=post_pk)

    # django 将用户提交的数据封装在 request.POST 中，这是一个类字典对象。
    # 我们利用这些数据构造了 CommentForm 的实例，这样就生成了一个绑定了用户提交数据的表单。
    form = CommentForm(request.POST)
    #当调用form.is_valid()方法时，django自动帮我们检查表单的数据是否符合格式要求
    if form.is_valid():
        #检查到数据是合法的，调用表单的save方法保存数据到数据库
        #commit=False的作用是仅仅利用表单的数据生成Comment模型类的实例，但还不保存评论数据到数据库
        comment=form.save(commit=False)
        
        #将评论和被评论的文章关联起来
        comment.post=post

        comment.save()
        messages.add_message(request,messages.SUCCESS,'评论发表成功!',extra_tags='success')

        #重定向到post的详情页，实际上党redirect函数接受一个模型的实例时，会调用这个模型实例的get_absolute_url方法，
        #然后重定向到get_absolute_url方法返回的url
        return redirect(post)
    
    #若检查到数据不合法，则渲染一个预览页面，用于展示表单的错误
    #注意这里被评论的文章post也传给了模板，因为我们需要根据port来生成表单的提交地址
    context={'post':post,
    'form':form,
    }
    messages.add_message(request,messages.ERROR,'评论发表失败！请修改表单中的错误后重新提交！',extra_tags='danger')
    return render(request,'comments/preview.html',context=context)

