from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .forms import 自定义注册表单, 自定义编辑表单, 自定义登陆表单
from .models import 普通会员表
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='myauth:登陆')
def 个人中心(请求):
    内容={ '用户':请求.user }
    return render (请求, 'myauth/个人中心.html', 内容)
@login_required(login_url='myauth:登陆')
    
def 编辑个人信息(请求):
    if 请求.method == 'POST':
        编辑表单 = 自定义编辑表单(请求.POST, instance=请求.user)
        if  编辑表单.is_valid():
            编辑表单.save()
            请求.user.普通会员表.昵称=编辑表单.cleaned_data['昵称']
            请求.user.普通会员表.生日=编辑表单.cleaned_data['生日']
            请求.user.普通会员表.save()
            # 普通会员表(用户=用户, 昵称=注册表单.cleaned_data['昵称'] , 生日=注册表单.cleaned_data['生日']).save()
            return redirect('myauth:个人中心')
    else:
        编辑表单 = 自定义编辑表单(instance=请求.user)
    内容 = {'编辑表单':编辑表单, '用户':请求.user}
    return render (请求, 'myauth/编辑个人信息.html', 内容)
@login_required(login_url='myauth:登陆')
    
def 修改密码(请求):
    if 请求.method == 'POST':
        改密表单 = PasswordChangeForm(data=请求.POST, user=请求.user)
        if  改密表单.is_valid():
            改密表单.save()

            return redirect('myauth:登陆')
    else:
        改密表单 = PasswordChangeForm(user=请求.user)
    内容 = {'改密表单':改密表单, '用户':请求.user}
    return render (请求, 'myauth/修改密码.html', 内容)

def 主页(请求):
    return render (请求, 'myauth/主页.html')

def 登陆(请求):
    if 请求.method == 'POST':
        登陆表单 = 自定义登陆表单(data=请求.POST)
        if  登陆表单.is_valid():
            用户 = authenticate(请求,username=登陆表单.cleaned_data['username'] , password=登陆表单.cleaned_data['password'])
            login(请求, 用户)
            return redirect('myauth:主页')      
    else:
        登陆表单 = 自定义登陆表单()
    内容 = {'登陆表单':登陆表单, '用户':请求.user}
    return render(请求, 'myauth/登陆.html', 内容)


def 注销(请求):
    logout(请求)
    return redirect('myauth:主页')
def 注册(请求):
    if 请求.method == 'POST':
        注册表单 = 自定义注册表单(请求.POST)
        if  注册表单.is_valid():
            注册表单.save()
            用户 = authenticate(请求,username=注册表单.cleaned_data['username'] , password=注册表单.cleaned_data['password1'])
            用户.email=注册表单.cleaned_data['email']
            普通会员表(用户=用户, 昵称=注册表单.cleaned_data['昵称'] , 生日=注册表单.cleaned_data['生日']).save()
            login(请求, 用户)
            return redirect('myauth:主页')

    else:
        注册表单 = 自定义注册表单()
    内容 = {'注册表单':注册表单}
    return render (请求, 'myauth/注册.html', 内容)