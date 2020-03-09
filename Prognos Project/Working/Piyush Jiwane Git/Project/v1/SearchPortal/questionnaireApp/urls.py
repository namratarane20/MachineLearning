from django.urls import path
from . import views
#
# urlpatterns = [
#     path('', views.userLogin),
#     path('mailVerification', views.mailVerification),
#     path('searchKeyword', views.searchKeyword),
#     path('uploadcsv', views.uploadcsv),
#     path('homepage', views.toHomePage),
#     path('indexfile', views.indexToElasticsearch)
# ]


urlpatterns = [
    path('', views.Home),
    path('searchKeyword', views.searchKeyword, name='tryFunc'),
    path('account/logout/', views.Logout),
    path('adminLogin', views.adminLogin),
    path('adminMailVerification', views.adminMailVerification),
    path('indexQuestionnaireFile', views.indexQuestionnaireFile),
    path('indexPoliciesFile', views.indexPoliciesFile),
    path('toHomePage', views.toHomePage),
    path('addToTags',views.addToTags),
    # path('dispalyTagName',views.dispalyTagName),
    path('destroyTag', views.destroyTagInformation),

    path("<str:tagname>", views.displayTagInformation, name='displayTagInfo'),
    path('displayTagInformation',views.displayTagInformation),
]
