from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('details/<int:id>/', views.DetailBookView.as_view(), name='detail_book'),
    path('book/<int:id>/add-review/', views.AddReview.as_view(), name='add_review'),
    # path('buy/<int:car_id>/', views.buy_car, name='buy_car')
]