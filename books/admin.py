from django.contrib import admin
from .models import Book, Purchase, Choice
# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['book']}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Purchase, QuestionAdmin)
admin.site.register(Book)