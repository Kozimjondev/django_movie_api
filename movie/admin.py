from django.contrib import admin
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
# Register your models here.
class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = "__all__"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', )
    list_display_links = ('name',)
# admin.site.register(Category, CategoryAdmin)

class ReviewInLine(admin.StackedInline):
    model = Review
    extra = 1
    readonly_fields = ('name', 'email')

class MovieShotsInLine(admin.StackedInline):
    model = MovieShots
    extra = 1

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    inlines = [MovieShotsInLine, ReviewInLine]
    save_on_top = True
    save_as = True
    form = MovieAdminForm
    list_editable = ('draft',)
    actions = ['publish', 'unpublish']
    fieldsets = (
        (None, {'fields': (('title', 'tagline'),)}),
        (None, {'fields': ('description', 'poster')}),
        (None, {'fields': (('year', 'world_premiere', 'country'),)}),
        ("Actors", {
            'classes': ('collapse',),
            'fields': (('actors', 'directors', 'genres', 'category'),)}),
        (None, {'fields': (('budget', 'fees_in_usa', 'fees_in_world'),)}),
        ("Options", {'fields': (('url', 'draft',),)}),
    )

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 record is updated"
        else:
            message_bit = f"{row_update} records are updated"
        self.message_user(request, f'{message_bit}')


    def publish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 record is updated"
        else:
            message_bit = f"{row_update} records are updated"
        self.message_user(request, f'{message_bit}')

    publish.allowed_permissions = ('change',)
    unpublish.allowed_permissions = ('change',)
# admin.site.register(Movie)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'parent', 'movie')
    list_display_links = ('name',)
    readonly_fields = ('name', 'email')
# admin.site.register(Review)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
# admin.site.register(Genre)

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'image')

# admin.site.register(Actor)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('star', 'movie', 'ip')
# admin.site.register(Rating)

@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie')
# admin.site.register(MovieShots)


admin.site.register(RatingStar)

admin.site.site_title = "Django movies"
admin.site.site_header = "Django movies"
