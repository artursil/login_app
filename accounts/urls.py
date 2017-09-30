from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r"login/$", auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    url(r"logout/$", auth_views.LogoutView.as_view(), name="logout"),
    url(r"signup/$", views.UserSignupView.as_view(), name="signup"),
    url(r"singup3/$", TemplateView.as_view(template_name="accounts/singup_complete.html"),name="signup3"),
    url(r"profile/(?P<username>[-\w]+)/$", views.UserTagsView.as_view(template_name="accounts/profile.html"), name="user_tags"),
    # url(r"profile2/(?P<username>[-\w]+)/$", views.UserTagsView.as_view(), name="user_tags"),
    url(r"profile/(?P<username>[-\w]+)/delete/(?P<slug>[-\w]+)$", views.UserTagDeleteView.as_view(), name="user_tag_delete"),
    url(r"profile/(?P<username>[-\w]+)/change-favourite-team/(?P<pk>\d+)/$", views.UserFavTeamChangeView.as_view(), name="change_fav_team"),
    url(r"profile/(?P<username>[-\w]+)/history/$", views.UserHistoryView.as_view(), name="user_history"),

]
