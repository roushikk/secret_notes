from django.contrib import admin

from . import models


class NoteAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'allowed_reads',
        'times_read',
        'display_confirmation',
        'created_at',
        'modified_at',
        'expires_at',
    )

    search_fields = (
        'title',
        'slug',
    )


admin.site.register(models.Note, NoteAdmin)
