from datetime import date

from django.db import models
from django.urls import reverse



# Create your models here.
class Category(models.Model):
    name = models.CharField("Category", max_length=100)
    description = models.TextField("Description")
    url = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Actor(models.Model):
    name = models.CharField("Name", max_length=100)
    age = models.PositiveSmallIntegerField("Age", default=0)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to='actors/')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("actor_detail", kwargs={'slug': self.name})

    class Meta:
        verbose_name = "Actor and directors"
        verbose_name_plural = "Actor and directors"


class Genre(models.Model):
    name = models.CharField("Name", max_length=100)
    description = models.TextField("description")
    url = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Movie(models.Model):
    title = models.CharField("Title", max_length=100)
    tagline = models.CharField("tagline", max_length=100, default='')
    description = models.TextField('description')
    poster = models.ImageField("poster", upload_to='movies/')
    year = models.PositiveSmallIntegerField("year", default=2020)
    country = models.CharField("country", max_length=100)
    directors = models.ManyToManyField(Actor, verbose_name='directors', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name="Actors", related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='genres')
    world_premiere = models.DateField("World premiere", default=date.today)
    budget = models.PositiveSmallIntegerField('Budget', default=0, help_text='show money in dollars')
    fees_in_usa = models.PositiveSmallIntegerField(
        'Fees in USA', default=0, help_text='show money in dollars')
    fees_in_world = models.PositiveSmallIntegerField(
        'Fees in the world', default=0, help_text='show money in dollars')
    category = models.ForeignKey(
        Category, verbose_name='Categories', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=100, unique=True)
    draft = models.BooleanField("Draft", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={'slug': self.url})

    def get_review(self):
        return self.review_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'


class MovieShots(models.Model):
    title = models.CharField("Trailers", max_length=100)
    description = models.TextField('Description')
    image = models.ImageField("Images", upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, verbose_name='Movie', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Trailers'
        verbose_name_plural = 'Trailers'


class RatingStar(models.Model):
    value = models.SmallIntegerField('Value', default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Star rating'
        verbose_name_plural = 'Star rating'


class Rating(models.Model):
    ip = models.CharField('IP address', max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='star')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='movie', related_name='ratings')

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Rating'


class Review(models.Model):
    email = models.EmailField()
    name = models.CharField('name', max_length=100)
    text = models.TextField('text', max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name='Parent', on_delete=models.SET_NULL, blank=True, null=True, related_name='children'
    )
    movie = models.ForeignKey(Movie, verbose_name='movie', on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'













