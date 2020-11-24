import re
from django.contrib.auth import login
from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.views import View
from django import http
from django.urls import reverse
from .models import User
from yyrear_mall.utils.response_code import RETCODE

# Create your views here.

class UsernameCountView(View):
    """判断用户名是否重复注册"""

    def get(self, request, username):
        """
        :param username: 用户名
        :return: JSON
        """
        # 接收和校验参数
        count = User.objects.filter(username=username).count()
        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})


class MobileCountView(View):
    """判断手机号是否重复"""

    def get(self, request, mobile):
        """
        :param mobile: 注册手机号
        :return: JSON
        """
        # 接收和校验参数
        count = User.objects.filter(mobile=mobile).count()
        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg':'OK', 'count':count})


class RegisterView(View):
    """用户注册"""

    def get(self, request):
        """提供用户注册页面"""
        return render(request, 'register.html')

    def post(self, request):
        """实现用户注册业务逻辑"""
        # 接收参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        allow = request.POST.get('allow')

        # 校验参数: 前后端的校验需要分开, 避免恶意用户越过前段逻辑发请求, 要保证后端安全, 前后端的校验逻辑相同
        # 判断参数是否齐全: all([列表]): 会去校验列表中的元素是否为空, 只要有一个为空, 返回false
        if not all([username, password, password2, mobile, allow]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断用户名是否是5-20位字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20位字符的用户名')
        # 判断密码是否是8-20位字符
        if not re.match(r'^[a-zA-Z0-9_-]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位字符的密码')
        # 判断确认密码是否与密码相同
        if password2 != password:
            return http.HttpResponseForbidden('两次密码输入不一致')
        # 判断手机号否正确
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        # 判断是否合法
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选同意用户协议')
        #return render(request, 'register.html', {'register_errmsg': '注册失败'})
        # 保存注册数据
        try:
            # 注册成功后返回user用户对象, 后面用于状态保持
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '注册失败'})

        # 实现状态保持
        login(request, user)

        # 响应结果
        # return redirect('/')
        return redirect(reverse('contents:index'))