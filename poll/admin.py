from django.contrib import admin

from .models import Poll, PollQuestion


class PollQuestionInline(admin.TabularInline):
    model = PollQuestion

class PollAdmin(admin.ModelAdmin):
    inlines = [
        PollQuestionInline
    ]

admin.site.register(Poll, PollAdmin)