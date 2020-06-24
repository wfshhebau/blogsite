
from django.urls import path, re_path
from  . import views
from . import list_views


app_name = 'article'
urlpatterns = [
    path("article/", views.article_column, name="article_column"),
    path('rename-column/', views.rename_article_column, name="rename_article_column"),
    path('del-column/',views.del_article_column,name="del_article_column"),
    path('article-post/',views.article_post, name="article_post"),
    path("article-list/",views.article_list, name="article_list"),

    # reverse url路径，还带参数
    #re_path('article-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.article_detail, name="article_detail"),  # 这个坑，坑死我了
    path('article-detail/<int:id>/<slug:slug>/', views.article_detail, name="article_detail"),

    path("del-article/", views.del_article, name="del_article"),
    path('redit-article/<int:article_id>/', views.redit_article, name="redit_article"),

    # 具有分页功能的文章列表
    path("article-list-paginate/",views.article_list_paginate,name="article_list_paginate"),

    # 文章标题展示，任何用户都可访问
    path("list-article-titles/",list_views.article_title,name="list_article_titles"),

    # 通过单击上面文章的标题，可以查看文章详情
    path("list-article-detail/<int:id>/<slug:slug>/",list_views.article_detail,name="list_article_detail"),
    #path('article-content/<int:id>/<slug:slug>/', list_views.article_detail, name="article_content"),

    # 通过点击list-article-titles上的作者名称，可以列出该作者名下的所有article titles
    path("author_article_titles/<username>/",list_views.author_article_titles,name="author_article_titles"),

    # P168 为文章点赞的url
    path("like-article/",list_views.like_article,name="like_article"),


    # p196 添加标签tag信息,并在leftslider中添加该url的超链接
    path('article-tag/',views.article_tag,name="article_tag"),

    #p199 删除标签
    path("del-artcicle-tag",views.del_article_tag,name="del_article_tag"),


    ]