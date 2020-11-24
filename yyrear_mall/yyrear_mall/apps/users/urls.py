from django.urls import path, re_path
from .views import RegisterView, UsernameCountView, MobileCountView

app_name="users"    # 根路由中include第三个参数
urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),    # 用户注册
    re_path('usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/', UsernameCountView.as_view()),   # 用户是否重复注册
    re_path('mobiles/(?P<mobile>1[3-9]\d{9})/count', MobileCountView.as_view()),    # 手机号是否重复
]