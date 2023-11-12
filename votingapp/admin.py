from django.contrib import admin
from .models import Poll, Answer

# Inline admin for Answers
class AnswerInline(admin.TabularInline):  # or use admin.StackedInline for a different layout
    model = Answer
    extra = 1  # Number of empty forms to display

# Custom admin for Poll
class PollAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]  # Add Answer inline

# Register Poll with the custom admin
admin.site.register(Poll, PollAdmin)
