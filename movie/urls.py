from .views import *
from django.urls import path
from .api import ActorViewSet

urlpatterns = [
    path('movie/', MovieListView.as_view()),
    path('movie/<int:pk>/', MovieDetailView.as_view()),
    path('review/', ReviewCreateView.as_view()),
    path('rating/', AddStarRatingView.as_view()),
    # path('actors/', ActorsListView.as_view()),
    # path('actors/<int:pk>/', ActorsDetailView.as_view()),

    path('actors/', ActorViewSet.as_view({'get': 'list'})),
    path('actors/<int:pk>/', ActorViewSet.as_view({'get': 'retrieve'})),
]
