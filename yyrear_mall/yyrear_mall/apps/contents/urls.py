from django.urls import path
from .views import IndexView

app_name = "contents"  # 根路由中include第三个参数
urlpatterns = [
    path('', IndexView.as_view(), name="index"),  # 首页
]
