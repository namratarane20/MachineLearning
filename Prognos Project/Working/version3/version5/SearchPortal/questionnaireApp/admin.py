from django.contrib import admin
from .models import TagWithInfo
from .models import RelevantData


class QuestionnaireAdmin(admin.ModelAdmin):
    admin.site.register(TagWithInfo)
    admin.site.register(RelevantData)


