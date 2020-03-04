from django.contrib import admin
from .models import TagWithInfo, Search,RelevantData


class QuestionnaireAdmin(admin.ModelAdmin):
    admin.site.register(TagWithInfo)

admin.site.register(Search)
admin.site.register(RelevantData)
