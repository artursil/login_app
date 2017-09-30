from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView, RedirectView, UpdateView
from django.shortcuts import redirect, reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from . import forms
from tags.models import Tags
from accounts.models import UserTags,UserProfile
from news.models import News, UserViewedNews
from django.http import Http404

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("accounts:signup2")
    template_name = "accounts/signup.html"

class UpdateProfile(CreateView):
    form_class = forms.UserUpdateForm
    success_url = reverse_lazy("accounts:signup3")
    template_name = "accounts/signup2.html"



class UserSignupView(CreateView):
    form_class = forms.UserCreationMultiForm
    success_url = reverse_lazy('accounts:signup3')
    template_name = "accounts/signup.html"

    # def form_valid(self, form):
    #     # Save the user first, because the profile needs a user before it
    #     # can be saved.
    #     user = form['user'].save()
    #     profile = form['profile'].save(commit=False)
    #     profile.UserProfile = user
    #     profile.save()
    #     return redirect(self.get_success_url())


class UserTagsView(LoginRequiredMixin, ListView):
    model=UserTags
    template_name="accounts/_user_tags_list.html"



    def get_queryset(self):
        try:
            self.user_now=self.kwargs.get("username")

            userprofile_id = UserProfile.objects.filter(UserProfile__username=self.user_now)[0].id
            self.tags = UserTags.objects.filter(user_id=userprofile_id).order_by("negative","tag__tag_name")
            # self.tags = self.tags[0].tag.tag_name
            # self.tags = Tags.objects.filter(userprofile__id=userprofile_id).order_by("tag_name")


        except UserTags.DoesNotExist:
            raise Http404
        else:
            return self.tags
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["tags"] = self.tags
            return context



class UserTagDeleteView(LoginRequiredMixin,RedirectView):

    def get(self, request, *args, **kwargs):
            user_tags = UserTags.objects.filter(
                user=self.request.user.userprofile,
                tag__slug=self.kwargs.get("slug")
            ).get()

            user_tags.delete()
            messages.success(
                self.request,
                "You have successfully delete this tag."
            )
            return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse("accounts:user_tags",kwargs={"username": self.kwargs.get("username")})
class UserHistoryView(LoginRequiredMixin,ListView):
    model=UserViewedNews
    template_name="accounts/user_history.html"

    def get_queryset(self):
        try:
            self.user_now=self.kwargs.get("username")
            userprofile_id = UserProfile.objects.filter(UserProfile__username=self.user_now)[0].id
            self.news_list = UserViewedNews.objects.filter(user__id=userprofile_id).order_by('created_at')
            # self.news_list = News.objects.filter(users__id=userprofile_id)

        except:
            raise Http404
        else:
            return self.news_list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["news_list"] = self.news_list
        return context

class UserFavTeamChangeView(LoginRequiredMixin, UpdateView):
    form_class = forms.UserUpdateForm
    model = UserProfile

    template_name = "accounts/_user_fav_team.html"

    def get_success_url(self):
        return reverse_lazy("accounts:user_tags",kwargs={"username": self.kwargs.get("username")})

    # def form_valid(self, form):
    #     # Save the user first, because the profile needs a user before it
    #     # can be saved.
    #     fav_team = form['fav_team']
    #     UserP=self.request.user.userprofile
    #     profile.UserProfile = user
    #     profile.save()
    #     return redirect(self.get_success_url())

# class UserTeams(LoginRequiredMixin,CreateView):
#     pass
