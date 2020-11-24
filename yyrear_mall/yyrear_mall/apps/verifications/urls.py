from django.urls import re_path
from .views import ImageCodeView


urlpatterns = [
    re_path('image_codes/(?P<uuid>[\w-]+)/', ImageCodeView.as_view()),  # 图形验证码
]