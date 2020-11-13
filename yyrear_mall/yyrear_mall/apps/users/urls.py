from django.urls import path, re_path
from .views import RegisterView, UsernameCountView

app_name="users"    # 根路由中include第三个参数
urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),    # 用户注册
    re_path('usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/', UsernameCountView.as_view()),   # 用户是否重复注册
]