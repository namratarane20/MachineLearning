from django.contrib import admin
from .models import TagWithInfo, Search


class QuestionnaireAdmin(admin.ModelAdmin):
    admin.site.register(TagWithInfo)

admin.site.register(Search)
