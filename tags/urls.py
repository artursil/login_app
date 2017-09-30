from django.conf.urls import url

from . import views
from django.views import generic
app_name = 'tags'

urlpatterns = [
    url(r"^$", generic.TemplateView.as_view(template_name="tags/_tags.html"),name="tags"),
    url(r"search/$",views.search_tags),
    url(r"tag_add/(?P<slug>[-\w]+)/(?P<negative>[-\w]+)/$",views.AddTagView.as_view(),name="tag_add"),
    url(r"tag_delete/(?P<slug>[-\w]+)/$",views.DeleteTagView.as_view(),name="tag_delete"),
    url(r"redirect/(?P<slug>[-\w]+)/$", views.RedirectTagView.as_view(), name="tag_redirect"),
    url(r"(?P<slug>[-\w]+)/$", views.TagsNewsListView.as_view(), name="tags_news"),


    # url(r"tag_ad/(?P<slug>[-\w]+)/$",views.AddTag.as_view(),name="tag_ad"),


]
