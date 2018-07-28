from django.conf.urls import url

from . import views

app_name = 'subjects'

urlpatterns = [
    url(r"^$", views.ListSubject.as_view(), name="all"),
    url(r"^new/$", views.CreateSubject.as_view(), name="create"),
    url(r"^posts/in/(?P<slug>[-\w]+)/$",views.SingleSubject.as_view(),name="single"),
    url(r"join/(?P<slug>[-\w]+)/$",views.FollowSubject.as_view(),name="follow"),
    url(r"leave/(?P<slug>[-\w]+)/$",views.UnfollowSubject.as_view(),name="unfollow"),
]
