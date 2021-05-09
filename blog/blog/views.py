from django.shortcuts import render
from django.template import loader
# Create your views here.
from django.http import HttpResponse
# from .models import Question
from django.http import Http404
from .models import Post


# 从模板文件夹下加载模板文件并将一个字典对象传入视图
def index(request):
    post_list=Post.objects.all().order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

# def details(request,question_id):
#     try:
#         question=Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("问卷不存在")
#     return render(request,'polls/detail.html',{'question':question})

# def results(request,question_id):
#     return HttpResponse("正在查看问卷%s的结果。"%question_id)

# def vote(request,question_id):
#     return HttpResponse("请为问卷%s提交您的答案。" % question_id)