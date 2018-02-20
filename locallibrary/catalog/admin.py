from django.contrib import admin
from .models import *


admin.site.register(Genre)
# admin.site.register(BookInstance)
# admin.site.register(Book)
# admin.site.register(Author)

# Inline Models
class BookInstaneInline(admin.TabularInline):
    model = BookInstance


class BookInline(admin.TabularInline):
    # tabular looks better then stack
    model = Book

# Admin Models
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

    inlines = [BookInline]


admin.site.register(Author, AuthorAdmin)
# or @admin.register(Author)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstaneInline]



@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back')

    # list filter will add a Filter division to filter result w.r.t list
    list_filter = ('status','due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )



