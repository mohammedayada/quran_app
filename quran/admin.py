from django.contrib import admin

# Register your models here.
from .models import (
    Part,
    Surah,
    Verse,
    Author,
    Explanation,
)


# @admin.register(Part)
# class PartAdmin(admin.ModelAdmin):
#     list_display = ("number", "from_verse", "to_verse")
#
#
# @admin.register(Surah)
# class SurahAdmin(admin.ModelAdmin):
#     list_display = ("id", "title", "numbers_of_verses", "madanya_or_makya")
#
#
# @admin.register(Verse)
# class VerseAdmin(admin.ModelAdmin):
#     list_display = ("id", "text", "surah", "number")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Explanation)
class ExplanationAdmin(admin.ModelAdmin):
    list_display = ("verse", "author")
