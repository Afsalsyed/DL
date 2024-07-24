from django.urls import path
from .views import *
from account.views import custom_logout
  


urlpatterns = [
    #Author Dashboard
    path('startnew/',startnew, name='startnew'),
    path('draft/',Draftview, name='draft'),
    path('submitted/',Submittedview, name='submitted'),
    path('revision/',Revisionview, name='revision'),
    path('accepted/',Acceptedview, name='accepted'),
    path('rejected/',Rejectedview, name='rejected'),
    #Submission flow
    path('new_submission/<int:submission_id>/', submission_step_one, name='new_submission'),
    path('submission_step_two/<int:submission_id>/',submission_step_two, name='submission_step_two'),
    path('step3/<int:submission_id>/', keyword, name='step3'),
    path('step4/<int:submission_id>/', add_authors_institutions, name='step4'),
    path('step5/<int:submission_id>/', step5, name='step5'),
    path('step6/<int:submission_id>/', step6_review_submit, name='step6_review_submit'),
    #File processsing
    path('submission/<int:submission_id>/view_proof/',view_proof, name='view_proof'),
    path('submission_step_six/<int:submission_id>/', submission_step_six, name='submission_step_six'),
    #test
    # path('submission/<int:submission_id>/add-authors-institutions/', add_authors_institutions, name='add_authors_institutions'),
    #logout
    path('logout/', custom_logout, name='logout'),
    #ajax
    path('add-coauthor-ajax/<int:submission_id>/', add_coauthor_ajax, name='add_coauthor_ajax'),
    path('remove-coauthor-ajax/<int:submission_id>/', remove_coauthor_ajax, name='remove_coauthor_ajax'),
]

