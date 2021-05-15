from django.urls import path
from . import views

app_name='blog'
urlpatterns=[
    path('',views.index,name='index'),
    path('posts/<int:pk>/',views.detail,name='detail'),
    path('archives/<int:year>/<int:month>/',views.archive,name='archive'),
    path('categories/<int:pk>/',views.category,name='category'),
    path('tags/<int:pk>/',views.tag,name='tag'),
    path('blogs/',views.blogs,name='blogs'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    # path('<int:question_id>/',views.details,name='detail'),
    # path('<int:question_id>/results/',views.results,name='results'),
    # path('<int:question_id>/vote/',views.vote,name='vote'),
]