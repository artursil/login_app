from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Count, Q
from django.utils import timezone
# from . import forms
from . import models
from django.contrib.auth import get_user_model
from accounts.models import UserTags, UserProfile
from datetime import date, datetime, timedelta
from news.tests import sort_order
from tags.models import Tags
import pandas as pd
import math
from django.http import Http404
from stats.views import  LeagueTableMixin, NextGameMixin , PlayerStatsMixin
from tags.views import TagsNewsMixin

User = get_user_model()
News=models.News
UserViewedNews=models.UserViewedNews


from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.core.urlresolvers import reverse


# Create your views here.
class NewsListView( generic.ListView):
     model=models.News

class UserNewsListView(LoginRequiredMixin, generic.ListView):
     model=models.News
     context_object_name='news_list'
     paginate_by = 2

     def get_sorting_order(self,q,total_views_today):
        news_list_df=pd.DataFrame(columns = ['pk','News','Views_cnt','Rating','Tweet','Fb_post'])
        tags_df = pd.DataFrame(list(self.news_user.values('id','newstags__tag')))

        for i in range(len(q)):
            news_title=str(q[i])
            users_count=int(q[i].users__count)
            pk=self.news_user[i].pk
            date_news=self.news_user[i].date_added
            tw_rating=0
            fb_rating=0
            tweet=self.news_user[i].tweet
            if tweet:
                tw_rating = self.news_user[i].favs + 8*self.news_user[i].retweets + 2*self.news_user[i].replies
            fb_post= self.news_user[i].fb_post
            if fb_post:
                fb_rating= self.news_user[i].fb_rating
            news_team=list(self.news_user[i].team.values_list("id",flat=True))
            #fav team
            fav_team_flg=0

            # for team in news_team:
            if self.userprofile_fav_team in news_team:
                    fav_team_flg =1
            #end fav
            # for tags
            tags_news_list = list(tags_df.loc[tags_df['id'] == int(pk)]['newstags__tag'])
            if math.isnan(tags_news_list[0]):
                tags_sum=0
            else:
                tags_sum=0
                for tag in tags_news_list:
                    if tag in self.tags_list:
                        tags_sum +=1
            if math.isnan(tags_news_list[0]):
                tags_neg_sum=0
            else:
                tags_neg_sum=0
                for tag in tags_news_list:
                    if tag in self.tags_list:
                        tags_neg_sum +=1
            # end for tags
            # for dates
            if date_news>(timezone.now() - timedelta(minutes=5)):
                date_rating=100000
            elif date_news>(timezone.now() - timedelta(minutes=15)):
                date_rating=1000
            elif date_news>(timezone.now() - timedelta(hours=3)):
                date_rating=100
            elif date_news>(timezone.now() - timedelta(hours=24)):
                date_rating=10
            else:
                date_rating=0
            #end for dates

            rating=fav_team_flg*10000 + users_count/max(total_views_today,1)*1000+tags_sum+ date_rating + tw_rating + fb_rating -1000000* tags_neg_sum
            news_list_df=news_list_df.append({'pk':pk,'News':news_title, 'Views_cnt':users_count, 'Rating':rating, 'Tweet':tweet,'Fb_post':fb_post},ignore_index=True)

        news_list_df=news_list_df.sort_values('Rating',ascending=False)
        self.pk_list=list(news_list_df['pk'])

     def get_queryset(self):

            self.user_now=self.kwargs.get("username")
            userprofile = UserProfile.objects.filter(UserProfile__username=self.user_now).values('id','fav_team__id')
            userprofile_id = userprofile[0]['id']
            self.userprofile_fav_team = userprofile[0]['fav_team__id']
            self.tags_list=list(UserTags.objects.filter(user=userprofile_id,negative=False).values_list('tag__id',flat=True))
            self.tags_list_neg=list(UserTags.objects.filter(user=userprofile_id,negative=True).values_list('tag__id',flat=True))
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # DO ZMIANY LICZBA GODZIN JAK JUŻ BĘDZIE CRAWLER
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            self.news_user = News.objects.filter( Q(date_added__gte=(datetime.now()-timedelta(hours=1048))))

            total_views_today=UserViewedNews.objects.filter(created_at__gte=(datetime.now()-timedelta(hours=24))).count()
            q = self.news_user.annotate(Count('users'))


            self.get_sorting_order(q,total_views_today)

            clauses = ' '.join(['WHEN news_news.id=%s THEN %s' % (pk, i) for i, pk in enumerate(self.pk_list)])
            ordering = 'CASE %s END' % clauses
            self.queryset = self.news_user.filter(pk__in=self.pk_list).extra(select={'ordering': ordering}, order_by=('ordering',))




            return self.queryset

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # get context tylko do testow
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["test"] = self.pk_list
        return context












class UserNewsListMixin(object):


     def get_sorting_order(self,q,total_views_today):
        news_list_df=pd.DataFrame(columns = ['pk','News','Views_cnt','Rating','Tweet','Fb_post'])
        tags_df = pd.DataFrame(list(self.news_user.values('id','newstags__tag')))

        for i in range(len(q)):
            news_title=str(q[i])
            users_count=int(q[i].users__count)
            pk=self.news_user[i].pk
            date_news=self.news_user[i].date_added
            tw_rating=0
            fb_rating=0
            tweet=self.news_user[i].tweet
            if tweet:
                tw_rating = self.news_user[i].favs + 8*self.news_user[i].retweets + 2*self.news_user[i].replies
            fb_post= self.news_user[i].fb_post
            if fb_post:
                fb_rating= self.news_user[i].fb_rating
            news_team=list(self.news_user[i].team.values_list("id",flat=True))
            #fav team
            fav_team_flg=0

            # for team in news_team:
            if self.userprofile_fav_team in news_team:
                    fav_team_flg =1
            #end fav
            # for tags
            tags_news_list = list(tags_df.loc[tags_df['id'] == int(pk)]['newstags__tag'])
            if math.isnan(tags_news_list[0]):
                tags_sum=0
            else:
                tags_sum=0
                for tag in tags_news_list:
                    if tag in self.tags_list:
                        tags_sum +=1
            if math.isnan(tags_news_list[0]):
                tags_neg_sum=0
            else:
                tags_neg_sum=0
                for tag in tags_news_list:
                    if tag in self.tags_list:
                        tags_neg_sum +=1
            # end for tags
            # for dates
            if date_news>(timezone.now() - timedelta(minutes=5)):
                date_rating=100000
            elif date_news>(timezone.now() - timedelta(minutes=15)):
                date_rating=1000
            elif date_news>(timezone.now() - timedelta(hours=3)):
                date_rating=100
            elif date_news>(timezone.now() - timedelta(hours=24)):
                date_rating=10
            else:
                date_rating=0
            #end for dates

            rating=fav_team_flg*10000 + users_count/max(total_views_today,1)*1000+tags_sum+ date_rating + tw_rating + fb_rating -1000000* tags_neg_sum
            news_list_df=news_list_df.append({'pk':pk,'News':news_title, 'Views_cnt':users_count, 'Rating':rating, 'Tweet':tweet,'Fb_post':fb_post},ignore_index=True)

        news_list_df=news_list_df.sort_values('Rating',ascending=False)
        self.pk_list=list(news_list_df['pk'])

     def get_queryset(self):

            self.user_now=self.kwargs.get("username")
            userprofile = UserProfile.objects.filter(UserProfile__username=self.user_now).values('id','fav_team__id')
            userprofile_id = userprofile[0]['id']
            self.userprofile_fav_team = userprofile[0]['fav_team__id']
            self.tags_list=list(UserTags.objects.filter(user=userprofile_id,negative=False).values_list('tag__id',flat=True))
            self.tags_list_neg=list(UserTags.objects.filter(user=userprofile_id,negative=True).values_list('tag__id',flat=True))
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # DO ZMIANY LICZBA GODZIN JAK JUŻ BĘDZIE CRAWLER
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            self.news_user = News.objects.filter( Q(date_added__gte=(datetime.now()-timedelta(hours=1048))))

            total_views_today=UserViewedNews.objects.filter(created_at__gte=(datetime.now()-timedelta(hours=24))).count()
            q = self.news_user.annotate(Count('users'))


            self.get_sorting_order(q,total_views_today)

            clauses = ' '.join(['WHEN news_news.id=%s THEN %s' % (pk, i) for i, pk in enumerate(self.pk_list)])
            ordering = 'CASE %s END' % clauses
            self.queryset = self.news_user.filter(pk__in=self.pk_list).extra(select={'ordering': ordering}, order_by=('ordering',))




            return self.queryset

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # get context tylko do testow
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["test"] = self.pk_list
        return context


















class PageUserNewsView(UserNewsListMixin,LeagueTableMixin,NextGameMixin, generic.ListView):
    model=News
    template_name="news/news_page.html"
    context_object_name='news_list'
    paginate_by=1



    def get_queryset(self):
        queryset = UserNewsListMixin.get_queryset(self)
        return queryset
    def get_context_data(self, **kwargs):
        context = LeagueTableMixin.get_context_data(self,**kwargs)
        context.update(NextGameMixin.get_context_data(self,**kwargs))
        return context

class PlayerNewsView(TagsNewsMixin,PlayerStatsMixin, generic.ListView):
    model=News
    template_name="news/news_player.html"
    context_object_name='news_list'
    paginate_by=1



    def get_queryset(self):
        slug=self.kwargs.get("slug")
        queryset = TagsNewsMixin.get_queryset(self,slug)
        return queryset
    def get_context_data(self, **kwargs):
        slug=self.kwargs.get("slug")
        context = TagsNewsMixin.get_context_data(self,slug, **kwargs)
        context.update(PlayerStatsMixin.get_context_data(self,slug, **kwargs))
        return context


class AddToNewsView(LoginRequiredMixin, generic.RedirectView):


    # def get_redirect_url(self, *args, **kwargs):
    #     return reverse("news:for_user",kwargs={"username": self.kwargs.get("username")})


    def get(self, request, *args, **kwargs):
        self.pk=self.kwargs.get("pk")
        news = get_object_or_404(News,pk=self.pk)

        try:
            models.UserViewedNews.objects.create(user=self.request.user.userprofile,news=news)
        except :
            messages.warning(self.request,("Warning, this user already read: {}".format(news.title)))

        else:
            messages.success(self.request,"This user read: {} news.".format(news.title))

        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        self.url= News.objects.filter(pk=self.pk).values("news_url")[0]['news_url']
        return self.url
