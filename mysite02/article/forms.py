from django import forms
from .models import ArticleColumn

#  创建文章标题表单
class AritcleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ("column",)


#  创建文章发布表单
from .models import ArticlePost
class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ("title","body")




# 创建评论表单类
from django import forms
from .models import Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("commentator","body",)


# 创建文章标签表单类
from  .models import ArticleTag
class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ("tag",)



