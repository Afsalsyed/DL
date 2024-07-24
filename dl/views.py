from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from oss.models import Journal 
from .models import *
from django.urls import reverse

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


def journal_detail(request, pk):
    journal = get_object_or_404(Journal, pk=pk)
    context = {
        'journal': journal
    }
    return render(request, 'test.html', context)

def volume_page(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    volumes = Volume.objects.filter(journal=journal)
    context = {
        'journal': journal,
        'volumes': volumes,
    }
    return render(request, 'volume_page.html', context)

def add_volume(request):
    if request.method == 'POST':
        print(request.POST)
        volume = request.POST.get('volume')
        description = request.POST.get('description')
        year = request.POST.get('year')
        journal_id = request.POST.get('journal_id')
        journal = get_object_or_404(Journal, id=journal_id)
        print(journal)

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
def issues_page(request):
    # Render the issues page template
    return render(request, 'issue_page.html')



#***********************************************************
def articles_page(request):
    # Render the articles page template
    return render(request, 'article_page.html')