from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 增加注册用户的生日和电话的信息标签
class UserProfile(models.Model):     # 这句话作用是，将在数据库中建立一个名为account_userprofile的表
    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True)      # 该类中的user字段(作为纽带)与User类之间的关系是一对一的
    birth = models.DateField(blank=True,null=True)
    phone = models.CharField(max_length=20,null=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)

# 创建存放个人信息的数据模型
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    school = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    aboutme = models.TextField(blank=True)
    photo = models.ImageField(blank=True)

    def __str__(self):
        return "user:{}".format(self.user.username)


