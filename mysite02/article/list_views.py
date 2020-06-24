# 这里新建另一个视图函数py库list_views.py

# -----------------------Redis数据库--------------------------------------------------------
# p176 建立Redis数据库连接
import redis
from django.conf import settings  # 导入settings中的设置，localhost，port等
r = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)
# -----------------------Redis数据库--------------------------------------------------------



# 创建一个用函于显示文章标题列表的函数，该数不需要登录，即任何用户都可以浏览文章标题
# 基于数据模型：ArticlePost,ArticleColumn
from .models import ArticlePost,ArticleColumn
from django.shortcuts import render
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def article_title(request):
    article_list = ArticlePost.objects.all()
    paginator = Paginator(article_list,2)   # per_page=2, 2 items/per_page
    page = request.GET.get('page')

    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
    finally:
        articles = current_page.object_list
    return render(request,"article/list/article_titles.html",{"articles":articles,"page":current_page})


# 再创建一个不用login就可以查看文章详细内容的函数，供文章标题的超链接使用
# 注意在views.py中，也有一个article_detail(),那个是针对于登录用户的，两者在不同py中，虽然名字相同，但互不影响
from django.shortcuts import get_object_or_404
from .models import ArticlePost, Comment
from .forms import CommentForm
from django.db.models import Count   # p203 推荐相似文章时使用
def article_detail(request,id,slug):
    article = get_object_or_404(ArticlePost,id=id,slug=slug)

    # +++++++++++++++浏览次数++++++++++
    # 记录浏览次数：每打开一次文章，浏览次数就+1； 文章以article.id标识
    total_views = r.incr("article:{}:views".format(article.id))  # p176,对象类型:对象ID:对象属性

    # +++++++++++++++实现热门++++++++++
    # 根据浏览次数，显示热门文章
    r.zincrby('article_ranking', 1, article.id)

    article_ranking = r.zrange("article_ranking", 0, -1, desc=True, withscores=False)[:10]   # 降序，前10
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids)) # 注双下划线
    most_viewed.sort(key =lambda x: article_ranking_ids.index(x.id))   # 需要再理解一下？？？？

    # +++++++++++++++实现评论++++++++++
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)   # ("commentator","body",)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
    else:
        comment_form = CommentForm()

    # +++++++++++++++实现推荐(4个)++++++++++
    article_tags_id = article.article_tag.values_list("id",flat=True)  # P202
    similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_id).exclude(id=article.id)
    # this_article_tags = article.article_tag.values_list("tag",flat=True)
    # similar_articles = ArticlePost.objects.filter(article_tag__tag__in=this_article_tags).exclude(id=article.id)
    similar_articles_sorted = similar_articles.annotate(same_tags=Count("article_tag")).order_by("-same_tags","-created")[:4]

    return render(request,"article/list/article_detail.html",{"article":article,
                                                              "total_views":total_views,
                                                              "most_viewed":most_viewed,
                                                              "comment_form":comment_form,
                                                              "similar_articles":similar_articles_sorted,
                                                              })

# 查看某个作者的所有的文章标题,如果有username就返回该作者的文章titles，如果没有username就返回所有文章的titles
from django.contrib.auth.models import User
from account.models import UserInfo

def author_article_titles(request, username=None):
    if username:
        user = User.objects.get(username=username)
        article_list = ArticlePost.objects.filter(author=user)
        userinfo = user.userinfo if user.userinfo else None     # 有些作者没有填写userinfo: school,company,phtoto...
    else:
        article_list = ArticlePost.objects.all()

    paginator = Paginator(article_list,2)   # per_page=2, 2 items/per_page
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
    finally:
        articles = current_page.object_list

    if username:
        # author_article_titles.html 带作者的userinfo信息
        return render(request,"article/list/author_article_titles.html",{"user":user,
                                                                         "userinfo":userinfo,
                                                                         "articles":articles,
                                                                         "page":current_page
                                                                         }
                      )
    else:
        return render(request,"article/list/article_titles.html",{"articles":articles,"page":current_page})


# P168
# 用户根据article的id，给出两种action：like or unlike
from . models import ArticlePost
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@csrf_exempt
@require_POST
@login_required(login_url="/account/login/")
def like_article(request):
    article_id = request.POST.get("id")       # id and action from web's post
    action = request.POST.get("action")
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action == "like":
                article.users_like.add(request.user)
                return HttpResponse("1")
            else:
                article.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("No")







