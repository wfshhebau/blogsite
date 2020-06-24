from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from .models import ArticleColumn
from .forms import AritcleColumnForm

# Create your views here.
@login_required(login_url='/account/login/')
@csrf_exempt
def article_column(request):
    if request.method == 'GET':
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = AritcleColumnForm()
        return render(request,'article/column/article_column.html',{"columns":columns,"column_form":column_form})
    if request.method == 'POST':
        column_name = request.POST['column']       # get column_name from Ajax
        columns = ArticleColumn.objects.filter(user_id=request.user.id, column=column_name)    # check whether column_name is exist?
        if columns:
            return HttpResponse("2")     # if column_name already exist
        else:
            ArticleColumn.objects.create(user=request.user,column=column_name)    # creat new item
            return HttpResponse("1")


# 编辑/重命名栏目名称
@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST["column_name"]
    column_id = request.POST["column_id"]      #column_id = request.POST.get("column_id","default")
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")


# 删除栏目
@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def del_article_column(request):
    column_id = request.POST["column_id"]      # "column_id"是AJAX的Post传过来的data名
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

# 文章发布 view fun
# p200-201 重新添加文章标签功能
from .models import ArticlePost
from .forms import ArticlePostForm
import json
@login_required(login_url='/account/login')
@csrf_exempt
def article_post(request):
    if request.method=="POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)    # title,body
                new_article.author = request.user   # author
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])  #column
                new_article.save()
                tags = request.POST['tags']          # tags
                if tags:
                    for atag in json.loads(tags):      # 不要忘记 import json
                        tag = request.user.tag.get(tag=atag)   # <==> tag = ArticleTag.objects.get(tag=atag)
                        new_article.article_tag.add(tag)
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    if request.method == 'GET':
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        article_tags = request.user.tag.all()
        return render(request, "article/column/article_post.html",{"article_post_form":article_post_form,
                                                                   "article_columns":article_columns,
                                                                   "article_tags":article_tags,
                                                                   }
                      )


# 显示文章标题列表函数(同时可显示文章所属栏目的信息),
from .models import ArticlePost
@login_required(login_url="/account/login/")
def article_list(request):
    articles = ArticlePost.objects.filter(author=request.user)
    return render(request,"article/column/article_list.html",{"articles":articles})



# 显示文章详情，需要两个参数，文章的id和文章的slug
# 参考.models.ArticlePost(models.Model)中的get_absolute_url(self)
from django.shortcuts import  get_object_or_404
from .models import ArticlePost
from account.models import UserInfo
@login_required(login_url="/account/login/")
def article_detail(request,id,slug):
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    userinfo = UserInfo.objects.get(user=request.user)     # 用于显示作者图片
    return render(request,"article/column/article_detail.html",{"article":article,"userinfo":userinfo})



# 删除article函数---删除已经发表的article，必须是POST，参数为article的id
from .models import ArticlePost
@login_required(login_url="/account/login/")
@require_POST
@csrf_exempt
def del_article(request):
    article_id = request.POST["article_id"]
    try:
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

# 重新编辑article函数---重新编辑已经发表的aticle，GET时读取并显示article，POST时修改并提交article
from .models import ArticlePost
from .forms import ArticlePostForm
@login_required(login_url="/account/login/")
@csrf_exempt
def redit_article(request,article_id):
    if request.method == "GET":
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id=article_id)
        this_article_form = ArticlePostForm(initial={"title":article.title})
        this_article_column = article.column
        return render(request,"article/column/redit_article.html",{ "article_columns":article_columns,
                                                                    "article":article,
                                                                    "this_article_form":this_article_form,
                                                                    "this_article_column":this_article_column,
                                                                    }
                      )

    if request.method == "POST":
        this_redit_article = ArticlePost.objects.get(id=article_id)
        try:
            this_redit_article.column = request.user.article_column.get(id=request.POST["column_id"])
            this_redit_article.title = request.POST["title"]
            this_redit_article.body = request.POST["body"]
            this_redit_article.save()
            return HttpResponse("1")
        except:
            return HttpResponse("2")


# 重写article_list(),引入分页功能
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import ArticlePost
@login_required(login_url="/account/login/")
def article_list_paginate(request):
    articles_list = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(articles_list,2)    #per_page=2,每页的项数
    page = request.GET.get("page")

    try:
        current_page = paginator.page(page)     # 正常读出请求页的页码，page必须>=1
    except PageNotAnInteger:
        current_page = paginator.page(1)        # 若请求的页码数值不是整数，则设定为第1页
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)    # 若请求的页码数值为空或没有page，则设定为总页数
    finally:
        articles = current_page.object_list      # 读出current_page下的所有article列表

    return render(request,"article/column/article_list_paginate.html",{"articles":articles,"page":current_page})


# 编写文章标签添加与显示的视图函数
from . models import ArticleTag
from . forms import ArticleTagForm
@login_required(login_url="/account/login/")
@csrf_exempt
def article_tag(request):
    if request.method == "GET":
        article_tags = ArticleTag.objects.filter(author=request.user)
        article_tag_form = ArticleTagForm()
        return render(request,'article/tag/tag_list.html',{"article_tags":article_tags,
                                                           "article_tag_form":article_tag_form
                                                           })
    if request.method == "POST":
        tag_post_form = ArticleTagForm(data=request.POST)
        if tag_post_form.is_valid():
            try:
                new_tag = tag_post_form.save(commit=False)
                new_tag.author = request.user
                new_tag.save()
                return HttpResponse("1")
            except:
                return HttpResponse("The tag cannot be save")
        else:
            return HttpResponse("Sorry,the form is not valid!")

# 编写标签删除的视图函数
@login_required(login_url="/account/login/")
@require_POST
@csrf_exempt
def del_article_tag(request):
    tag_id = request.POST['tag_id']
    try:
        tag = ArticleTag.objects.get(id=tag_id)
        tag.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

