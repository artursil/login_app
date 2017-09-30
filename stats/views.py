from django.shortcuts import render
from tags.models import Team, League
from stats.models import TeamStats, Season, Game , PlayerStats
from django.utils import timezone
from datetime import  timedelta
from django.db.models import Q
from django.views import generic
from django.http import Http404

# Create your views here.
class LeagueTableListView( generic.ListView):
     model=TeamStats
     template_name = "stats/league_table.html"

     def get_queryset(self):
        try:
            self.slug=self.kwargs.get("slug")
            self.league= Team.objects.filter(slug=self.slug)[0].league
            self.team_stats= TeamStats.objects.filter(competition__league=self.league, competition__league_flg=True, season__date_end__gte=timezone.now()).order_by("-points")


        except TeamStats.DoesNotExist:
            raise Http404
        else:
            return self.team_stats

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["league"] = self.league
        return context

class LeagueTableMixin(object):

     def get_queryset(self):

            user=self.request.user
            self.league= Team.objects.filter(favteams__UserProfile=user)[0].league
            self.team_stats= TeamStats.objects.filter(competition__league=self.league, competition__league_flg=True, season__date_end__gte=timezone.now()).order_by("-points")



            return [self.team_stats,self.league]

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        LeagueTableMixin.get_queryset(self)
        context["team_stats"] = self.team_stats
        context["league"] = self.league
        return context

class NextGameView( generic.ListView):
     model=Game
     template_name = "stats/next_game.html"

     def get_queryset(self):
        try:
            self.slug=self.kwargs.get("slug")
            self.nextgame=Game.objects.filter(Q(Team_home__slug=self.slug) | Q(Team_away__slug=self.slug), Date_game__gte=(timezone.now()-timedelta(hours=2)))[0]
            if self.nextgame.Date_game<=timezone.now():
                self.minute="15"
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# jak będzie podpięty ajax to spróbować na żywo z livescore'a ciągnąc
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            else:
                self.minute=""


        except Game.DoesNotExist:
            raise Http404
        else:
            return self.nextgame

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["next_game"] = self.nextgame
        context["minute"] = self.minute

        return context

class NextGameMixin(object):
     model=Game
     def get_queryset(self):
        try:
            user = self.request.user
            self.nextgame=Game.objects.filter(Q(Team_home__favteams__UserProfile=user) | Q(Team_away__favteams__UserProfile=user), Date_game__gte=(timezone.now()-timedelta(hours=2)))[0]
            if self.nextgame.Date_game<=timezone.now():
                self.minute="15"
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# jak będzie podpięty ajax to spróbować na żywo z livescore'a ciągnąc
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            else:
                self.minute=""


        except :
            raise Http404
        else:
            return self.nextgame

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        NextGameMixin.get_queryset(self)
        context["next_game"] = self.nextgame
        context["minute"] = self.minute

        return context


class FixturesListView(generic.ListView):
    model=Game
    template_name = "stats/fixtures.html"
    paginate_by=10

    def get_queryset(self):
        try:
            user=self.request.user
        except:
            self.fixtures=Game.objects.filter(Date_game__gte=(timezone.now()-timedelta(hours=2)))
        else:
            self.fixtures=Game.objects.filter(Q(Team_home__favteams__UserProfile=user) | Q(Team_home__favteams__UserProfile=user), Date_game__gte=(timezone.now()-timedelta(hours=2)))
        return self.fixtures

class ResultsListView(generic.ListView):
    model=Game
    template_name = "stats/results.html"
    paginate_by=10

    def get_queryset(self):
        try:
            user=self.request.user
        except:
            self.results=Game.objects.filter(Date_game__gte=(timezone.now()-timedelta(hours=2)))
        else:
            self.results=Game.objects.filter(Q(Team_home__favteams__UserProfile=user) | Q(Team_home__favteams__UserProfile=user), Date_game__lte=(timezone.now()-timedelta(hours=2)))
        return self.results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["results"] = self.results
        return context

class FixturesSearchListView(generic.ListView):
    model=Game
    template_name = "stats/search_fixtures.html"
    paginate_by=10

    def get_queryset(self):
        self.slug=self.kwargs.get("slug")
        self.search_fixtures=Game.objects.filter(slug=self.slug, Date_game__lte=(timezone.now()-timedelta(hours=2)))
        return self.seach_fixtures

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["seach_fixtures"] = self.seach_fixtures
        return context

class PlayerStatsMixin(object):

     def get_queryset(self,slug):
        try:
            self.player_stats= PlayerStats.objects.filter(player__slug=slug, season__date_end__gte=timezone.now())[0]

        except:
            raise Http404
        else:
            return self.player_stats

     def get_context_data(self,slug, **kwargs):
        context = super().get_context_data(**kwargs)
        PlayerStatsMixin.get_queryset(self,slug)
        context["player_stats"] = self.player_stats
        return context
