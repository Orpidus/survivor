from django.urls import path

from user.views import SurvivorRegisterView, UserInformationView, AdvocateRegisterView

urlpatterns = [
    path('survivor/', SurvivorRegisterView.as_view(), name='survivor-register'),
    path('advocate/', AdvocateRegisterView.as_view(), name='advocate-register'),
    path('<int:user_id>/', UserInformationView.as_view(), name='user-information'),
]
