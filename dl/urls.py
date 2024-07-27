from django.urls import path
from account.views import user_management
from .views import *

urlpatterns = [
    path('', bridge, name='bridge'),
    #User management
    path('user_management/', user_management, name='user_management'),
    #Volume
    path('volume_page/<int:journal_id>/', volume_page, name='volume_page'),
    path('add_volume/', add_volume, name='add_volume'),
    path('edit_volume/', edit_volume, name='edit_volume'),
    #Issue
    path('issues/<int:journal_id>/', issue_list, name='issue_list'),
    path('issues/save/', save_issue, name='save_issue'),
    #Article
    path('article_publish_page/<int:journal_id>/', article_publish_page, name='articles_page'),
    path('publish_article/', publish_article, name='publish_article'),  # New URL for publishing
 


]
