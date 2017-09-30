from django.conf.urls import url

from . import views
from django.views import generic

app_name = 'stats'

urlpatterns = [
    # url(r"^$", views.NewsListView.as_view(), name="all"),
    url(r"table/(?P<slug>[-\w]+)/$",views.LeagueTableListView.as_view(),name="table_view"),
    url(r"nextgame/(?P<slug>[-\w]+)/$",views.NextGameView.as_view(),name="next_game_view"),
    url(r"fixtures/$",views.FixturesListView.as_view(),name="fixtures_view"),
    url(r"results/$",views.ResultsListView.as_view(),name="fixtures_view"),




]
