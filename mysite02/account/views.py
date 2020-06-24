from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login


# Create your views here.
from .forms import LoginForm
def user_login(request):
    if request.method == "POST":
        login_form  = LoginForm(request.POST)
        if login_form.is_valid():
            login_data = login_form.cleaned_data
            user = authenticate(username=login_data['username'],password=login_data['password'])
            if user:
                login(request, user)
                return HttpResponse("Welcome! you have login successfully")
            else:
                return HttpResponse("Sorry,Your username or password is not right")
        else:
            return HttpResponse("Invalaid Login")

    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "account/login_better.html", {"form":login_form})     # login.html or login_better.html


# Creat register fun
from .forms import RegistrationForm
from .forms import UserProfileForm
#from .forms import UserInfo                # 后加的，用吗？
def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            #UserInfo.objects.create(user=new_user)     # 后加的，用吗？
            return HttpResponse('New user registered successfully')
        else:
            return HttpResponse('Sorry,Your registration failed!')
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request,"account/register.html",{"form":user_form,"profile":userprofile_form})


# Creat display 用户个人信息的 fun,从多个表中获取个人信息并展示
# 要显示用户个人信息，必须要求用户处于登录状态，若没有登录，会跳转到登录页面
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile, UserInfo
@login_required(login_url='/account/login/')  # 若未登陆，跳转到登陆页面
def myself(request):
    user = request.user
    userprofile = UserProfile.objects.get(user=user) if hasattr(user, 'userprofile') else UserProfile.objects.create(user=user)
    userinfo = UserInfo.objects.get(user=user) if hasattr(user, 'userinfo') else UserInfo.objects.create(user=user)
    return render(request, "account/myself.html", {"user":user, "userprofile":userprofile, "userinfo":userinfo})

    #-------------------------以下这段程序也可以用于展示-------------------------------------
    # user = request.user
    # userprofile = UserProfile.objects.get(user=user)
    # userinfo = UserInfo.objects.get(user=user)
    # return render(request, "account/myself.html",
    #               {"user": user, "userprofile": userprofile, "userinfo": userinfo})
    #-------------------------以上这段程序也可以用于展示-------------------------------------


# Creat edit 编辑用户个人信息的 fun
# 要编辑个人信息，必须登录，若没有登录，会跳转到登录页面
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import UserForm, UserProfileForm, UserInfoForm
@login_required(login_url='/account/login/')
def myself_edit(request):
    user = request.user
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            user.save()
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('/account/my-information/')  # 个人信息编辑后跳转到个人信息显示页面
    else:
        user_form = UserForm(instance=user)
        userprofile_form = UserProfileForm(initial={"birth":userprofile.birth,"phone":userprofile.phone})
        userinfo_form = UserInfoForm(initial={"school":userinfo.school,
                                              "company":userinfo.company,
                                              "profession":userinfo.profession,
                                              "address":userinfo.address,
                                              "aboutme":userinfo.aboutme,
                                              "photo": userinfo.photo
                                              }
                                     )
        return render(request,"account/myself_edit.html",{"user":user,
                                                          "userinfo":userinfo,
                                                          "user_form":user_form,
                                                          "userprofile_form":userprofile_form,
                                                          "userinfo_form":userinfo_form}
                      )



# 用户图片处理函数
from django.contrib.auth.decorators import login_required
from .models import UserInfo
@login_required(login_url='/account/login/')
def my_image(request):
    if request.method == 'POST':
        img = request.POST['img']
        userinfo = UserInfo.objects.get(user=request.user.id)
        userinfo.photo = img
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request, 'account/imagecrop.html',)
