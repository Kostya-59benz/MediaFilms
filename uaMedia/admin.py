from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe 
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from modeltranslation.admin import TranslationAdmin

from .models import Category, Rating, RatingStar, Actor, Movie, MovieShots, Genre, Reviews


class MovieAdminForm(forms.ModelForm):
    description_ru = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategotyAdmin(TranslationAdmin):
    """Категории"""
    list_display = ("id", "name", "url")
    list_display_links =("name", )



class ReviewInline(admin.TabularInline):
    """ Отзывы на странице фильма"""
    model= Reviews
    extra = 1
    readonly_fields = ('name', 'email')
   
class MovieShotsInline(admin.TabularInline):
    model= MovieShots
    extra = 1
    readonly_fields = ("get_image",)


    def get_image(self,obj):
        return mark_safe(f'<img src={obj.image.url} width="70" height="100"')

    get_image.short_description = "Изображение"
    

@admin.register(Movie)
class MovieAdmin(TranslationAdmin):
    """Фильмы"""
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("category__name", "title", )
    inlines =  [MovieShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    actions =["publish", "unpublish"]
    readonly_fields = ("get_image",)
    form = MovieAdminForm

    fieldsets= (
        (None, {
            "fields":(("title","tagline"),)
        }),
        (None, {
            "fields": ("description", ("poster","get_image"))
        }),
        (None, {
            "fields": ("year", "world_premiere", "country")
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres"),)
        }),
        (None, {
 
            "fields": (("budget", "fees_in_usa", "fees_in_world"),)
        }),
        ("Options", {
            "fields": ("url", "draft")
        }),

    )

    def get_image(self,obj):
        return mark_safe(f'<img src={obj.poster .url} width="70" height="100"')

    
    
    def unpublish(self,request, queryset,):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены!"
        self.message_user(request, f"{message_bit}")        
    

    
    def publish(self,request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены!"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change',)


    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)



    get_image.short_description = "Постер"




@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email", 'text')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")

@admin.register(Actor)
class ActorAdmin(TranslationAdmin):
    """Актеры"""
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)


    def get_image(self,obj):
        return mark_safe(f'<img src={obj.image.url} width="70" height="70"')

    get_image.short_description = "Изображение"

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("movie", "ip")
    readonly_fields = ("movie", "ip")



@admin.register(MovieShots)
class MovieShotsAdmin(TranslationAdmin):
    """Кадры из фильма"""
    list_display = ("title", "movie", "get_image")

    readonly_fields = ("get_image",)


    def get_image(self,obj):
        return mark_safe(f'<img src={obj.image.url} width="70" height="70"')

    get_image.short_description = "Изображение"

admin.site.register(RatingStar)

admin.site.site_title = "UA-MEDIA"
admin.site.site_header = "UA-MEDIA "


