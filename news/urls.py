from django.conf.urls import url

from . import views
from django.views import generic

app_name = 'news'

urlpatterns = [
    url(r"^$", views.NewsListView.as_view(), name="all"),
    url(r"for/(?P<username>[-\w]+)/$", views.UserNewsListView.as_view(), name="for_user"),
    url(r"page/(?P<username>[-\w]+)/$", views.PageUserNewsView.as_view(), name="page_user"),
    url(r"player/(?P<slug>[-\w]+)/$", views.PlayerNewsView.as_view(), name="page_player"),
    url(r"^page/for2/(?P<username>[-\w]+)/$", generic.TemplateView.as_view(template_name="news/news_page.html"),name="testas2"),
    url(r"add/(?P<username>[-\w]+)/(?P<pk>\d+)/$", views.AddToNewsView.as_view(), name="add_to_post"),



]
