from django.shortcuts import render
from news.models import News
from accounts.models import UserTags, UserProfile
from django.contrib.auth import get_user_model
from .models import Tags, Team
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from stats.models import Player
# Create your views here.

User = get_user_model()


class TagsNewsListView( generic.ListView):
     model=News
     template_name = "tags/tags_list.html"
     paginate_by= 10




     def get_queryset(self):
        try:
            self.slug=self.kwargs.get("slug")
            self.tags= Tags.objects.filter(slug=self.slug)
            main_tag=self.tags[0].main_tag
            if main_tag !=None:
                self.slug=Tags.objects.filter(tag_name=self.tags[0].main_tag)[0].slug
            self.news_list = News.objects.filter(news_tags__slug=self.slug)[:100]
            self.tag = get_object_or_404(Tags,slug=self.slug)


        except News.DoesNotExist:
            raise Http404
        else:
            return self.news_list

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            self.users=User.objects.filter(userprofile__tags__slug=self.slug)
            self.negative=UserTags.objects.filter(user=self.request.user.userprofile,tag=self.tag).values("negative")
        except:
            self.negative= ""
            context["tag_users"] = ""
        else:
            context["tag_users"] = self.users

        context["tag"] = self.tag
        if len(self.negative)>0:
            context["negative"] = self.negative[0]['negative']
        return context

class RedirectTagView(generic.RedirectView):

    # url="http//www.google.com"
    def get(self, request, *args, **kwargs):
        self.slug=self.kwargs.get("slug")
        self.players= list(Player.objects.filter().values_list("slug",flat=True))
        self.teams = list(Team.objects.filter().values_list("slug",flat=True))

        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if self.slug in self.players:
            return reverse("news:page_player",kwargs={"slug": self.kwargs.get("slug")})
        elif self.slug in self.teams:
            return reverse("tags:tags_news",kwargs={"slug": self.kwargs.get("slug")})
        else:
            return reverse("tags:tags_news",kwargs={"slug": self.kwargs.get("slug")})
class TagsNewsMixin(object):

     def get_queryset(self,slug):
        try:
            self.slug=slug
            self.tags= Tags.objects.filter(slug=self.slug)
            main_tag=self.tags[0].main_tag
            if main_tag !=None:
                self.slug=Tags.objects.filter(tag_name=self.tags[0].main_tag)[0].slug
            self.news_list = News.objects.filter(news_tags__slug=self.slug)[:100]
            self.tag = get_object_or_404(Tags,slug=self.slug)


        except :
            raise Http404
        else:
            return self.news_list

     def get_context_data(self,slug, **kwargs):
        context = super().get_context_data(slug,**kwargs)
        TagsNewsMixin.get_queryset(self,slug)
        try:
            self.users=User.objects.filter(userprofile__tags__slug=slug)
            self.negative=UserTags.objects.filter(user=self.request.user.userprofile,tag=self.tag).values("negative")
        except:
            self.negative= ""
            context["tag_users"] = ""
        else:
            context["tag_users"] = self.users

        context["tag"] = self.tag
        if len(self.negative)>0:
            context["negative"] = self.negative[0]['negative']
        return context



class AddTagView(LoginRequiredMixin, generic.RedirectView):

    # url="http//www.google.com"
    def get(self, request, *args, **kwargs):
        self.slug=self.kwargs.get("slug")
        negative=self.kwargs.get("negative")
        tag = get_object_or_404(Tags,slug=self.slug)

        try:
            UserTags.objects.create(user=self.request.user.userprofile,tag=tag,negative=negative)
        except :
            messages.warning(self.request,("Warning, you already have added tag: {}".format(tag.tag_name)))

        else:
            messages.success(self.request,"This user added tag: {} .".format(tag.tag_name))

        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse("tags:tag_redirect",kwargs={"slug": self.kwargs.get("slug")})

class DeleteTagView(LoginRequiredMixin, generic.RedirectView):



    def get(self, request, *args, **kwargs):

        try:

            user_tags = UserTags.objects.filter(
                user=self.request.user.userprofile,
                tag__slug=self.kwargs.get("slug")
            ).get()

        except :
            messages.warning(
                self.request,
                "You can't dalete this tag because you haven't added it."
            )
        else:
            user_tags.delete()
            messages.success(
                self.request,
                "You have successfully delete this tag."
            )
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse("tags:tag_redirect",kwargs={"slug": self.kwargs.get("slug")})

def search_tags(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
        # search_text="a"
        if search_text > '':
            tags = Tags.objects.filter(tag_name__icontains=search_text)
        else:
            tags= Tags.objects.none()
            text = 1
    else:
        search_text = ''
    return render(request, "tags/ajax_search.html", {'tags':tags})
