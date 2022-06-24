from django.urls import include, path

from article.views import (ArticleDelete, ArticleDetails, ArticleEdit,
                           ArticleList, AsView, GetCookie, GetSession,
                           OrderView, SetCookie, SetSession, t_jsonRes, test)

app_name = 'article'
urlpatterns = [
    path('ArticleList', ArticleList, name="ArticleList"),
    path('ArticleDetails/<int:id>', ArticleDetails,
         name="ArticleDetails"),  #路径后面加上id的值
    path('ArticleDelete/<int:id>/', ArticleDelete, name="ArticleDelete"),
    path('ArticleEdit', ArticleEdit, name="ArticleEdit"),
    path('ArticleEdit/<int:id>/', ArticleEdit, name="ArticleEdit"),
    path('test/<int:id1>/<int:id2>', test, name="test"),
    path('test/json', t_jsonRes, name="t_jsonRes"),
    path('test/setcookie', SetCookie, name="SetCookie"),
    path('test/getcookie', GetCookie, name="GetCookie"),
    path('test/setsession', SetSession, name="SetSession"),
    path('test/getsession', GetSession, name="GetSession"),
    path('test/as_view', AsView.as_view(), name="AsView"),
    path('test/orderview', OrderView.as_view(), name="OrderView"),
]
