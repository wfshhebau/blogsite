from django.conf.urls import url
from django.urls import path
from .import views
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
# from django.contrib.auth.views import LoginView       # 引入django的内置登录视图类
# from django.contrib.auth.views import LogoutView      # 引入django的内置OUT视图类
#
# from django.contrib.auth.views import PasswordChangeView
# from django.contrib.auth.views import PasswordChangeDoneView
# from django.contrib.auth.views import PasswordResetView
# from django.contrib.auth.views import PasswordResetConfirmView
# from django.contrib.auth.views import PasswordResetCompleteView
# from django.contrib.auth.views import PasswordResetDoneView

app_name = 'account'
urlpatterns = [
    # url(r'^login/$', views.user_login, name='user_login'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name="account/login.html"), name="user_login"),
    #以上是使用django的内置方法实现登录，并直接模板渲染，优点，1不用自己编写登录函数 2 可直接进行模板渲染 3 方便重定向

    #下面是使用django的内置方法实现退出
    # url(r'^logout/$',LogoutView.as_view(),name='user_logout'),   # LogoutView.as_view()将使用registration/logged_out.html
    url(r'^logout/$',auth_views.LogoutView.as_view(template_name='account/logout.html'),name='user_logout'),

    # 自定义的register view 实现注册
    url(r'^register/$', views.register, name="user_register"),

    # 使用内置方法实现密码Change
    url(r'^password-change/', auth_views.PasswordChangeView.as_view(
        template_name='account/password_change_form.html',
        success_url = reverse_lazy('account:password_change_done')),name='password_change'),   # 注意这个success_url

    url(r'^password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='account/password_change_done.html'), name='password_change_done'),

    # 使用内置方法实现密码Reset
    path('password-reset/',auth_views.PasswordResetView.as_view(
        template_name='account/password_reset_form.html',
        email_template_name='account/password_reset_email.html',
        subject_template_name = 'account/password_reset_subject.txt',
        success_url=reverse_lazy('account:password_reset_done')),name='password_reset'),    # success_url='/account/password-reset-done/'
    path('password-reset-done/',auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'),name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset_confirm.html',
        success_url = reverse_lazy('account:password_reset_complete')),name='password_reset_confirm'),   # success_url='/account/password-reset-complete/'
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'),name='password_reset_complete'),


    # 用户个人信息展示url
    path('my-information/',views.myself,name='my_information'),
    # 用户个人信息编辑url
    path('edit-my-information/',views.myself_edit,name='edit_my_information'),
    # 用户个人图片信息的url
    path('my-image/',views.my_image,name='my_image')

]