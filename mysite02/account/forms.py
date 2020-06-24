from django import forms
from django.contrib.auth.models import User

# 登录表单类
class LoginForm(forms.Form):    # 继承Form类，与继承ModelForm类区分
    username = forms.CharField(max_length=30)
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)  # widget用于规定元素类型


# 用户注册表单类
class RegistrationForm(forms.ModelForm):  # 继承ModelForm类
    password = forms.CharField(label="Password",widget=forms.PasswordInput,min_length=6)
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords do not match!")
        return cd["password2"]

# 增加注册内容的表单类，增加了生日和电话域
from .models import UserProfile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("birth","phone")


# 创建用户信息UserInfoForm表单类
from  .models import UserInfo
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("school","company","profession","address","aboutme","photo")

# 创建一个针对Django默认的auth_user库的表单类
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)   # 还有"username"，"first_name","last_name","date_joined","last_login"...