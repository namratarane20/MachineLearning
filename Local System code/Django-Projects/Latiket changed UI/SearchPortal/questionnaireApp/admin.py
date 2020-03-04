from django.contrib import admin
from .models import TagWithInfo, Search, RelevantResponseDatabase, UserSessionDatabase, KeywordSearchedDatabase, \
    MostFavouredResponseHistoryDatabase, FileUploadReport, AdminDB, QuestionDB


class QuestionnaireAdmin(admin.ModelAdmin):
    admin.site.register(TagWithInfo)


admin.site.register(Search)
admin.site.register(RelevantResponseDatabase)
admin.site.register(UserSessionDatabase)
admin.site.register(KeywordSearchedDatabase)
admin.site.register(MostFavouredResponseHistoryDatabase)
admin.site.register(FileUploadReport)
admin.site.register(AdminDB)
admin.site.register(QuestionDB)
