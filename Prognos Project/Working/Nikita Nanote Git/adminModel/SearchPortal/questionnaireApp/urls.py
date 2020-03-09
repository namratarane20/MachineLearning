from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home),
    path('searchKeyword', views.searchKeyword),
    path('searchKeyword/<str:recentSearch>', views.recentSearchKeyword, name="recentSearchKeyword"),
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
    path("tagInfo/<str:tagname>", views.displayTagInformation, name='displayTagInfo'),
    path("uploadFile", views.uploadFile),
    path("report", views.report),
    path("fillQuestionnaire/<str:vendorName>", views.fillQuestionnaire),
    path("toAdminHomePage", views.toAdminHomePage),
    path('uploadNewQuestionnaire', views.uploadNewQuestionnaire),
]
