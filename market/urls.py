from django.urls import path

from market import views

urlpatterns = [
    path("", views.home, name="home"),
    path("listings/new/", views.listing_new, name="listing_new"),
    path("listings/<int:pk>/", views.listing_detail, name="listing_detail"),
    path("listings/<int:pk>/edit/", views.listing_edit, name="listing_edit"),
    path("listings/<int:pk>/sold/", views.listing_sold, name="listing_sold"),
    path("listings/<int:pk>/delete/", views.listing_delete, name="listing_delete"),
    path("listings/<int:pk>/message/", views.start_thread, name="start_thread"),
    path("me/", views.mine, name="mine"),
    path("threads/<int:pk>/", views.thread_detail, name="thread_detail"),
    path("register/", views.register, name="register"),
    path("login/", views.sign_in, name="sign_in"),
    path("profile/", views.profile, name="profile"),
    path("desk/", views.desk, name="desk"),
]
