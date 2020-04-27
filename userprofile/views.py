from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from userprofile.models import Profile
from .forms import UserLoginForm, UserRegisterForm, ProfileForm

# Create your views here.

#用户登录
from userprofile.forms import UserLoginForm
from django.contrib.auth.models import User
# 引入验证登录的装饰器
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect("daily:list")
            else:
                return HttpResponse("账号或密码输入有误。请重新输入~")
        else:
            return HttpResponse("账号或密码输入不合法")
    else:
        return render(request, 'user/login.html')

# 用户退出
def user_logout(request):
    logout(request)
    return redirect("daily:list")

# 用户注册
def user_register(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname', '')
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 用户昵称不能为空
            if nickname:
                profile = Profile.objects.create(user=new_user,nikename=nickname)
                profile.save()
            else:
                return HttpResponse("用户昵称不能为空")

            # 保存好数据后立即登录并返回日报页面
            login(request, new_user)
            return redirect("daily:list")
        else:
            return HttpResponse("输入表单有误，所有字段都不能为空，请重新输入~")
    else:
        user_register_form = UserRegisterForm()
        context = { 'form': user_register_form }
        return render(request, 'user/register.html', context)



# 编辑用户信息
def profile_edit(request, id):
    user = User.objects.get(id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        # 验证修改数据者，是否为用户本人
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息。")

        profile_form = ProfileForm(request.POST)

        if profile_form.is_valid():
            # 取得清洗后的合法数据
            profile.nikename = profile_form.cleaned_data['nikename']
            profile.save()
            # 带参数的 redirect()
            return redirect("userprofile:edit", id=id)
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")

    else:
        context = {'profile': profile, 'user': user}
        return render(request, 'user/edit.html', context)
