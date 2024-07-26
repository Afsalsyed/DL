from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from oss.models import Journal, Accepted_Submission
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
    # Render the articles page template
    return render(request, 'article_publish_page.html', {'journal': journal})