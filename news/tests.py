from django.test import TestCase

# Create your tests here.
def sort_order(q,total_views_today):
  news_list_df=pd.DataFrame(columns = ['id','News','Views_cnt','Rating'])

  for i in range(len(q)):
    news_title=str(q[i])
    users_count=int(q[i].users__count)
    rating=users_count/total_views_today
    news_list_df=news_list_df.append({'id':i,'News':news_title, 'Views_cnt':users_count, 'Rating':rating},ignore_index=True)

  news_list_df=news_list_df.sort_values('Rating',ascending=False)
  return news_list_df
