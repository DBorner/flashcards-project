from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("try/start/<int:fishcardset_id>", views.start_try, name="start_try"),
    path("try/card/<int:try_card_id>", views.TryCardView.as_view(), name="try_card"),
    path(
        "try/finish/<int:user_try_id>",
        views.UserTryDetailView.as_view(),
        name="try_detail",
    ),
    path("try/restore/<int:user_try_id>", views.restore_try, name="restore_try"),
    path("try", views.UserTriesView.as_view(), name="try_list"),
    path("logout", views.logout_view, name="logout"),
    path("login", views.LoginPageView.as_view(), name="login"),
    path("register", views.RegisterPageView.as_view(), name="register"),
    path("change_password", views.ChangePasswordPageView.as_view(), name="change_password"),
]
