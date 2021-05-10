from django.urls import path
from . import views

app_name='blog'
urlpatterns=[
    path('',views.index,name='index'),
    path('posts/<int:pk>/',views.detail,name='detail'),
    # path('<int:question_id>/',views.details,name='detail'),
    # path('<int:question_id>/results/',views.results,name='results'),
    # path('<int:question_id>/vote/',views.vote,name='vote'),
]