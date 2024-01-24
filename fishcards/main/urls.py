from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('try/start/<int:fishcardset_id>', views.start_try, name='start_try'),
    path('try/card/<int:try_card_id>', views.TryCardView.as_view(), name='try_card'),
]
