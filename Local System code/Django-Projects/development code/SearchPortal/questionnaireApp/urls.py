from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.Home),
    path('searchKeyword', views.searchKeyword),
    path('recentSearchKeyword', views.recentSearchKeyword, name="recentSearchKeyword"),
    path('recentSearched',views.recentSearched, name="recentSearched"),
    path('account/logout/', views.Logout),
    path('adminLogin', views.adminLogin),
    path('adminMailVerification', views.adminMailVerification),
    path('indexQuestionnaireFile', views.indexQuestionnaireFile),
    path('indexPoliciesFile', views.indexPoliciesFile),
    path('toHomePage', views.toHomePage),
    path('relevantResponses', views.relevantResponses),
    path('addToTags', views.addToTags),
    path('destroyTag', views.destroyTagInformation),
    path('displayTagInformation', views.displayTagInformation),
    path('tagsAndFavouredResponse', views.tagsAndFavouredResponse),
    path("tagInfo", views.displayTagInformation, name='displayTagInfo'),
    path("uploadFile", views.uploadFile),
    path("report", views.report),
    path("fillQuestionnaire/<str:clientId>/", views.fillQuestionnaire),
    path("toAdminHomePage", views.toAdminHomePage),
    path('uploadNewQuestionnaire', views.uploadNewQuestionnaire),
    path('newQuestionnaireUpload', views.uploadNewQuestionnaireToDatabase),
    path("questionnaireDetails/<str:clientId>", views.questionnaireDetails),
]