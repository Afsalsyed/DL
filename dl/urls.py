from django.urls import path
from .views import *

urlpatterns = [
    path('', bridge, name='bridge'),
    #Volume
    path('volume_page/<int:journal_id>/', volume_page, name='volume_page'),
    path('add_volume/', add_volume, name='add_volume'),
    path('edit_volume/', edit_volume, name='edit_volume'),
    #Issue
    path('issues_page/<int:journal_id>/', issues_page, name='issues_page'),
    #Article
    path('articles_page/<int:journal_id>/', articles_page, name='articles_page'),
 


]
