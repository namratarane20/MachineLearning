from django.contrib import admin
from .models import TagWithInfo, Search,RelevantResponseDatabase,Image


class QuestionnaireAdmin(admin.ModelAdmin):
    admin.site.register(TagWithInfo)


admin.site.register(Search)
admin.site.register(RelevantResponseDatabase)
admin.site.register(Image)
