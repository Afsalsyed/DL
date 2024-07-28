from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from oss.models import Article_Status, Journal, Accepted_Submission, Submission
from .models import *
from django.urls import reverse
from .forms import *
# Create your views here.

#from accounts to DL
def bridge(request):
    if request.method == 'POST':
        journal_id = request.POST.get('journal_id')
        if not journal_id:
            return JsonResponse({'status': 'error', 'message': 'No journal ID provided'})

        try:
            journal = Journal.objects.get(id=journal_id)
            # Process the journal data as needed

            # Assuming you have a URL pattern named 'journal_detail' to display journal details
            redirect_url = reverse('volume_page', args=[journal_id])
            return JsonResponse({'status': 'success', 'redirect_url': redirect_url})
        except Journal.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Journal not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def volume_page(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    volumes = Volume.objects.filter(journal=journal).order_by('-id')
    latest_issue = Issue.objects.filter(volume__journal=journal).order_by('-id').first()
    latest_year = volumes.first().year if volumes.exists() else None

    context = {
        'journal': journal,
        'volumes': volumes,
        'latest_issue': latest_issue,
        'latest_year': latest_year,
    }
    return render(request, 'volume_page.html', context)


# def volume_page(request, journal_id):
#     journal = get_object_or_404(Journal, id=journal_id)
#     volumes = Volume.objects.filter(journal=journal).order_by('-id')
#     context = {
#         'journal': journal,
#         'volumes': volumes,
#     }
#     return render(request, 'volume_page.html', context)

def add_volume(request):
    if request.method == 'POST':
        volume = request.POST.get('volume')
        description = request.POST.get('description')
        year = request.POST.get('year')
        journal_id = request.POST.get('journal_id')
        journal = get_object_or_404(Journal, id=journal_id)

        Volume.objects.create(volume=volume, description=description, year=year, journal=journal)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def edit_volume(request):
    if request.method == 'POST':
        volume_id = request.POST.get('id')
        volume = request.POST.get('volume')
        description = request.POST.get('description')
        year = request.POST.get('year')

        volume_instance = get_object_or_404(Volume, id=volume_id)
        volume_instance.volume = volume
        volume_instance.description = description
        volume_instance.year = year
        volume_instance.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


#***********************************************
def issue_list(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    volumes = Volume.objects.filter(journal_id=journal_id).order_by('-id')
    issues = Issue.objects.filter(volume__in=volumes).order_by('-id')
    return render(request, 'issue_list.html', { 'issues': issues,'volumes': volumes,'journal': journal})



def save_issue(request):
    if request.method == 'POST':
        issue_id = request.POST.get('issueId')
        issue_text = request.POST.get('issue')
        volume_id = request.POST.get('volume')
        description = request.POST.get('description')

        if not issue_text or not volume_id or not description:
            return JsonResponse({'success': False, 'error': 'All fields are required'})

        try:
            volume = Volume.objects.get(id=volume_id)
        except Volume.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Volume not found'})

        if issue_id:  # Update existing issue
            issue = get_object_or_404(Issue, id=issue_id)
            issue.issue = issue_text
            issue.volume = volume
            issue.description = description
        else:  # Create new issue
            issue = Issue(issue=issue_text, volume=volume, description=description)

        issue.save()

        return JsonResponse({
            'success': True,
            'issue': {
                'id': issue.id,
                'issue': issue.issue,
                'volume_id': issue.volume.id,
                'volume': issue.volume.volume,
                'description': issue.description,
            }
        })

    return JsonResponse({'success': False, 'error': 'Invalid request method'})



#***********************************************************
def article_publish_page(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    accepted_submissions = Accepted_Submission.objects.filter(submission__journal=journal, submission__article_status__article_status='Proof read done')
    issues = Issue.objects.filter(volume__journal__id=journal_id).order_by('-id')  # Latest first
    volumes = Volume.objects.filter(journal_id=journal_id).order_by('-id')  # Latest first

    context = {
        'journal': journal,
        'accepted_submissions': accepted_submissions,
        'issues': issues,
        'volumes': volumes,
    }
    return render(request, 'article_publish_page.html', context)

def publish_article(request):
    if request.method == 'POST':
        print(request.POST)
        acceptedSubmission_id = request.POST.get('accepted_submission_id')
        issue = request.POST.get('issue_id')
        published_on = request.POST.get('published_on')

        accepted_submission = Accepted_Submission.objects.get(id=acceptedSubmission_id)
        
        published_article = Published_article.objects.create(
            accepted_submission=accepted_submission,
            issue_id=issue,
            published_on_date=published_on,
            doi='your-doi-here'  # You can generate or assign a DOI as needed
        )
        accepted_submission.submission.article_status = Article_Status.objects.get(article_status='Published')
        accepted_submission.submission.save()
        return JsonResponse({'success': True, 'message': 'Article published successfully!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request.'})

     