from django.urls import path
from .views import *

urlpatterns = [
    path('', bridge, name='bridge'),
    #Volume
    path('volume_page/<int:journal_id>/', volume_page, name='volume_page'),
    path('add_volume/', add_volume, name='add_volume'),
    path('edit_volume/', edit_volume, name='edit_volume'),
    #Issue
    path('issues/', issue_list, name='issue_list'),
    path('issues/save/', save_issue, name='save_issue'),
    #Article
    path('articles_page/', article_page, name='articles_page'),
 


]
