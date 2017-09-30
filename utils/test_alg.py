from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Count, Q
from django.utils import timezone
# from . import forms
from news import models
from django.contrib.auth import get_user_model
from accounts.models import UserTags, UserProfile
from datetime import date, datetime, timedelta
from news.tests import sort_order
from tags.models import Tags
import pandas as pd
import math
from django.http import Http404

User = get_user_model()
News=models.News
UserViewedNews=models.UserViewedNews


from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.core.urlresolvers import reverse



news_list_df=pd.DataFrame(columns = ['pk','News','Views_cnt','Rating'])
tags_df = pd.DataFrame(list(news_user.values('id','newstags__tag')))

for i in range(len(q)):
       news_title=str(q[i])
       users_count=int(q[i].users__count)
       pk=news_user[i].pk
       date_news=news_user[i].date_added
       tw_rating = news_user[i].favs + news_user[i].retweets + news_user[i].replies
       tw_rating= -99999999999
       news_team=list(news_user[i].team.values_list("id",flat=True))
       fav_team_flg=0


       if userprofile_fav_team in news_team:
               fav_team_flg =1

       tags_news_list = list(tags_df.loc[tags_df['id'] == int(pk)]['newstags__tag'])
       if math.isnan(tags_news_list[0]):
           tags_sum=0
       else:
           tags_sum=0
           for tag in tags_news_list:
               if tag in tags_list:
                   tags_sum +=1

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


       rating=fav_team_flg*10000 + users_count/max(total_views_today,1)*1000+tags_sum+ date_rating + tw_rating
       news_list_df=news_list_df.append({'pk':pk,'News':news_title, 'Views_cnt':users_count, 'Rating':rating},ignore_index=True)

   news_list_df=news_list_df.sort_values('Rating',ascending=False)
   pk_list=list(news_list_df['pk'])




user_now="splasi"
userprofile = UserProfile.objects.filter(UserProfile__username=user_now).values('id','fav_team__id')
userprofile_id = userprofile[0]['id']
userprofile_fav_team = userprofile[0]['fav_team__id']
tags_list=list(Tags.objects.filter(userprofile__id=userprofile_id).values_list('id',flat=True))
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # DO ZMIANY LICZBA GODZIN JAK JUŻ BĘDZIE CRAWLER
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
news_user = News.objects.filter( Q(date_added__gte=(datetime.now()-timedelta(hours=1048))))

total_views_today=UserViewedNews.objects.filter(created_at__gte=(datetime.now()-timedelta(hours=24))).count()
q = news_user.annotate(Count('users'))


            get_sorting_order(q,total_views_today)

clauses = ' '.join(['WHEN news_news.id=%s THEN %s' % (pk, i) for i, pk in enumerate(pk_list)])
ordering = 'CASE %s END' % clauses
queryset = news_user.filter(pk__in=pk_list).extra(select={'ordering': ordering}, order_by=('ordering',))





































news_title=str(q[i])
users_count=int(q[i].users__count)
pk=news_user[i].pk
date_news=news_user[i].date_added
tw_rating = news_user[i].favs + news_user[i].retweets + news_user[i].replies
tw_rating= 0
news_team=list(news_user[i].team.values_list("id",flat=True))
fav_team_flg=1

tags_news_list = list(tags_df.loc[tags_df['id'] == int(pk)]['newstags__tag'])
if math.isnan(tags_news_list[0]):
           tags_sum=0
else:
           tags_sum=0
           for tag in tags_news_list:
               if tag in tags_list:
                   tags_sum +=1

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


rating=fav_team_flg*10000 + users_count/max(total_views_today,1)*1000+tags_sum+ date_rating + tw_rating
news_list_df=news_list_df.append({'pk':pk,'News':news_title, 'Views_cnt':users_count, 'Rating':rating},ignore_index=True)

news_list_df=news_list_df.sort_values('Rating',ascending=False)
pk_list=list(news_list_df['pk'])
