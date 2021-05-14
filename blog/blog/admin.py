from django.contrib import admin

# Register your models here.

from .models import Post,Category,Tag

#使得后台显示Post更加详细的信息
class PostAdmin(admin.ModelAdmin):
    list_display=['text_title','created_time','modified_time','category','author']
    fields=['text_title','text_body','text_abstract','category','tags','author']
    def save_model(self,request,obj,form,change):
        obj.author=request.user
        super().save_model(request,obj,form,change)

admin.site.register(Post,PostAdmin)#使得后台能够修改相应的表
admin.site.register(Category)
admin.site.register(Tag)
