from django.urls import path
from . views import UserRegistrationView,UserLoginView,UserLogoutView,UserAccountUpdateView,BorrowedBooksView,pass_change

urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/',BorrowedBooksView.as_view(),name='profile'),
    path('profile/edit_profile', UserAccountUpdateView.as_view(), name='edit_profile' ),
    path('profile/change_password', pass_change, name='pass_change' ),
    
]