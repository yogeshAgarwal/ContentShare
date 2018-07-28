from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.urls import reverse
from django.db import IntegrityError
from django.views import generic
from django.shortcuts import get_object_or_404
from subjects.models import Subject, SubjectFollower
from . import models
# Create your views here.


class CreateSubject(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    model = Subject

class SingleSubject(generic.DetailView):
    model = Subject

class ListSubject(generic.ListView):
    model = Subject


class FollowSubject(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("subjects:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        subject = get_object_or_404(Subject,slug=self.kwargs.get("slug"))

        try:
            SubjectFollower.objects.create(user=self.request.user,subject=subject)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(subject.name)))

        else:
            messages.success(self.request,"You are now a member of the {} subject.".format(subject.name))

        return super().get(request, *args, **kwargs)


class UnfollowSubject(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("subjects:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            following = models.SubjectFollower.objects.filter(
                user=self.request.user,
                subject__slug=self.kwargs.get("slug")
            ).get()

        except models.SubjectFollower.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this Subject because you aren't in it."
            )
        else:
            following.delete()
            messages.success(
                self.request,
                "You have successfully left this subject."
            )
        return super().get(request, *args, **kwargs)
