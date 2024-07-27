from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from oss.models import Article_Status, Journal, Accepted_Submission
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
    context = {
        'journal': journal,
        'volumes': volumes,
    }
    return render(request, 'volume_page.html', context)

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
        form = IssueForm(request.POST)

        if form.is_valid():
            if issue_id:  # Update existing issue
                issue = Issue.objects.get(id=issue_id)
                form = IssueForm(request.POST, instance=issue)
            else:  # Create new issue
                issue = form.save(commit=False)

            issue = form.save()

            return JsonResponse({
                'success': True,
                'issue': {
                    'id': issue.id,
                    'issue': issue.issue,
                    'volume': issue.volume.volume,
                    'description': issue.description,
                }
            })

    return JsonResponse({'success': False, 'error': 'Invalid form data'})



#***********************************************************
def article_publish_page(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    accepted_submissions = Accepted_Submission.objects.filter(submission__journal_id=journal_id)
    issues = Issue.objects.filter(volume__journal__id=journal_id).order_by('-id')  # Latest first
    volumes = Volume.objects.filter(journal_id=journal_id).order_by('-id')  # Latest first

    return render(request, 'article_publish_page.html', {
        'journal': journal,
        'accepted_submissions': accepted_submissions,
        'issues': issues,
        'volumes': volumes,
    })

def publish_article(request):
    if request.method == 'POST':
        accepted_submission_id = request.POST.get('accepted_submission_id')
        issue_id = request.POST.get('issue_id')
        published_on = request.POST.get('published_on')

        try:
            accepted_submission = Accepted_Submission.objects.get(id=accepted_submission_id)
            # Get the Article_Status instance for "Published"
            published_status = Article_Status.objects.get(article_status='Published')
            # Update article status to published
            accepted_submission.submission.article_status = published_status # Set the foreign key to the Published status
            accepted_submission.submission.save()

            # Create a new Published_article instance
            published_article = Published_article.objects.create(
                accepted_submission_id=accepted_submission_id,
                issue_id=issue_id,
                published_on_date=published_on,
                doi='your-doi-here'  # You can generate or assign a DOI as needed
            )
            
            return JsonResponse({'success': True, 'message': 'Article published successfully!'})
        except Accepted_Submission.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Accepted Submission not found.'})
        except Article_Status.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Article Status not found.'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})