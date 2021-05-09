from django.contrib import admin

# Register your models here.

from .models import Post,Category,Tag

admin.site.register(Post)#使得后台能够修改Question表
admin.site.register(Category)
admin.site.register(Tag)
