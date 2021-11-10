from django.contrib import admin
from django.urls import path, include,re_path
from django.conf import settings
from django.conf.urls.static import static
from login import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index/', views.index),
    path('home/', views.home),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('addPage/',views.buildCourse,name="创建课程"),
    path('addCoursePage/',views.addCourse,name="创建课程页面"),
    path('testPage/',views.test,name="测试页面返回response"),
    

    
]

handler404 = 'login.views.page_not_found'
handler500 = 'login.views.page_error'

# 未解决问题 debug = true 时 页面出现静态文件 404
# python manage.py runserver --insecure