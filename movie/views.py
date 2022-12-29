from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from django.db import models
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Movie, Actor
from .service import get_client_ip, MovieFilter
from .paginators import MovieAPIListPagination



class MovieListView(ListAPIView):
    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = MovieAPIListPagination

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
               rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
            ).annotate(
                middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
            )
        return movies

# class MovieListView(APIView):
#     def get(self, request):
#         movies = Movie.objects.filter(draft=False).annotate(
#            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(request)))
#         ).annotate(
#             middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
#         )
#         serializer = MovieListSerializer(movies, many=True)
#         return Response(serializer.data)


class MovieDetailView(APIView):
    def get(self, request, pk):
        movie = Movie.objects.get(id=pk)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class ReviewCreateView(CreateAPIView):
    serializer_class = ReviewCreateSerializer

# class ReviewCreateView(APIView):
#     def post(self, request):
#         review = ReviewCreateSerializer(data=request.data)
#         if review.is_valid():
#             review.save()
#         return Response(status=201)



class AddStarRatingView(CreateAPIView):
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))

# class AddStarRatingView(APIView):
#     def post(self, request):
#         serializer = CreateRatingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(ip=get_client_ip(request))
#             return Response(status=201)
#         return Response(status=400)


# class ActorsListView(ListAPIView):
#     queryset = Actor.objects.all()
#     serializer_class = ActorListSerializer
#
#
# class ActorsDetailView(RetrieveAPIView):
#     queryset = Actor.objects.all()
#     serializer_class = ActorDetailSerializer
