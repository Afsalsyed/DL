from django.http import JsonResponse
from .models import Submission
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from account.models import Author

#Draft menu
@login_required
def Draftview(request):
    submissions = Submission.objects.filter(article_status__article_status='Draft', author=request.user)
    has_draft = Submission.objects.filter(article_status__article_status='Draft', author=request.user).exists()
    has_submitted = Submission.objects.filter(article_status__article_status='Submitted', author=request.user).exists()
    has_revision = Submission.objects.filter(article_status__article_status__in=['Minimum Revision' , 'Maximum Revision'], author=request.user).exists()
    has_accepted = Submission.objects.filter(decision__decision='Accepted', author=request.user).exists()
    has_rejected = Submission.objects.filter(decision__decision='Rejected', author=request.user).exists()

    if request.method =="POST":
        action = request.POST.get('action')
        submission_id = request.POST.get('submission_id')
        if action == 'delete' and submission_id:
            submission = Submission.objects.get(id=submission_id)
            submission.delete()
            return redirect('draft')
    return render(request, 'draftview.html', {
        'submissions': submissions,
        'has_draft':has_draft,
        'has_submitted': has_submitted,
        'has_revision': has_revision,
        'has_accepted': has_accepted,
        'has_rejected': has_rejected,
    })


#Submitted menu
@login_required
def Submittedview(request):
    submissions = Submission.objects.filter(article_status__article_status='Submitted', author=request.user)
    has_draft = Submission.objects.filter(article_status__article_status='Draft', author=request.user).exists()
    has_submitted = Submission.objects.filter(article_status__article_status='Submitted', author=request.user).exists()
    has_revision = Submission.objects.filter(article_status__article_status__in=['Minimum Revision' , 'Maximum Revision'], author=request.user).exists()
    has_accepted = Submission.objects.filter(decision__decision='Accepted', author=request.user).exists()
    has_rejected = Submission.objects.filter(decision__decision='Rejected', author=request.user).exists()
    return render(request, 'submittedview.html', {
        'submissions': submissions,
        'has_draft':has_draft,
        'has_submitted': has_submitted,
        'has_revision': has_revision,
        'has_accepted': has_accepted,
        'has_rejected': has_rejected,
    })

#New submission start
@login_required
def startnew(request):
    has_draft = Submission.objects.filter(article_status__article_status='Draft', author=request.user).exists()
    has_submitted = Submission.objects.filter(article_status__article_status='Submitted', author=request.user).exists()
    has_revision = Submission.objects.filter(article_status__article_status__in=['Minimum Revision' , 'Maximum Revision'], author=request.user).exists()
    has_accepted = Submission.objects.filter(decision__decision='Accepted', author=request.user).exists()
    has_rejected = Submission.objects.filter(decision__decision='Rejected', author=request.user).exists()
    return render(request,'start-new-submission.html',{
        'has_draft':has_draft,
        'has_submitted': has_submitted,
        'has_revision': has_revision,
        'has_accepted': has_accepted,
        'has_rejected': has_rejected,
    })

#Revision menu
@login_required
def Revisionview(request):
    submissions = Submission.objects.filter(article_status__article_status__in=['Minimum Revision' , 'Maximum Revision'], author=request.user)
    has_draft = Submission.objects.filter(article_status__article_status='Draft', author=request.user).exists()
    has_submitted = Submission.objects.filter(article_status__article_status='Submitted', author=request.user).exists()
    has_revision = Submission.objects.filter(article_status__article_status__in=['Minimum Revision' , 'Maximum Revision'], author=request.user).exists()
    has_accepted = Submission.objects.filter(decision__decision='Accepted', author=request.user).exists()
    has_rejected = Submission.objects.filter(decision__decision='Rejected', author=request.user).exists()
    return render(request,'revisionview.html', {
        'submissions': submissions,
        'has_draft':has_draft,
        'has_submitted': has_submitted,
        'has_revision': has_revision,
        'has_accepted': has_accepted,
        'has_rejected': has_rejected,
    })

#Accepted menu
@login_required
def Acceptedview(request):
    submissions = Submission.objects.filter(decision__decision='Accepted', author=request.user)
    has_draft = Submission.objects.filter(article_status__article_status='Draft', author=request.user).exists()
    has_submitted = Submission.objects.filter(article_status__article_status='Submitted', author=request.user).exists()
    has_revision = Submission.objects.filter(article_status__article_status__in=['Minimum Revision' , 'Maximum Revision'], author=request.user).exists()
    has_accepted = Submission.objects.filter(decision__decision='Accepted', author=request.user).exists()
    has_rejected = Submission.objects.filter(decision__decision='Rejected', author=request.user).exists()
    return render(request,'acceptedview.html', {
        'submissions': submissions,
        'has_draft':has_draft,
        'has_submitted': has_submitted,
        'has_revision': has_revision,
        'has_accepted': has_accepted,
        'has_rejected': has_rejected,
    })

#Rejected menu
@login_required
def Rejectedview(request):
    submissions = Submission.objects.filter(decision__decision='Rejected', author=request.user)
    has_draft = Submission.objects.filter(article_status__article_status='Draft', author=request.user).exists()
    has_submitted = Submission.objects.filter(article_status__article_status='Submitted', author=request.user).exists()
    has_revision = Submission.objects.filter(article_status__article_status__in=['Minimum Revision' , 'Maximum Revision'], author=request.user).exists()
    has_accepted = Submission.objects.filter(decision__decision='Accepted', author=request.user).exists()
    has_rejected = Submission.objects.filter(decision__decision='Rejected', author=request.user).exists()
    return render(request,'rejectedview.html', {
        'submissions': submissions,
        'has_draft':has_draft,
        'has_submitted': has_submitted,
        'has_revision': has_revision,
        'has_accepted': has_accepted,
        'has_rejected': has_rejected,
    })

#Step-1
@login_required
def submission_step_one(request, submission_id):
    submission = None  # to store already entered data 
    if submission_id:
        try:
            submission = Submission.objects.get(id=submission_id)
        except Submission.DoesNotExist:
            submission_id = None

    if request.method == 'POST':
        form = SubmissionStepOneForm(request.POST, instance=submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.author = request.user
            if not submission.manuscript_id:
                submission.manuscript_id = f"MSS-{submission.author.id}-{Submission.objects.count() + 1}"
                submission.article_status_id=get_object_or_404(Article_Status, article_status="Draft").id
            submission.save()
            request.session['submission_id'] = submission.id
            if 'save_and_continue' in request.POST:
                return redirect('submission_step_two', submission_id=submission.id)
            else:
                return render(request, 'begin-new-submission.html', {
                    'form': form,
                    'article_types': Article_Type.objects.all(),
                    'categories': Category.objects.all(),
                    'journals' : Journal.objects.all(),
                    'saved': True
                })
    else:
        form = SubmissionStepOneForm(instance=submission)

    return render(request, 'begin-new-submission.html', {
        'form': form,
        'article_types': Article_Type.objects.all(),
        'categories': Category.objects.all(),
        'journals' : Journal.objects.all(),
    })

#Step-3
@login_required
def keyword(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            keyword_text = request.POST.get('keyword')
            if keyword_text:
                keyword = Keyword.objects.create(submission=submission, keyword=keyword_text)
                return JsonResponse({'success': True, 'keyword': keyword.keyword, 'keyword_id': keyword.id})
            
        elif action == 'remove':
            keyword_id = request.POST.get('keyword_id')
            Keyword.objects.filter(id=keyword_id, submission=submission).delete()
            return JsonResponse({'success': True, 'keyword_id': keyword_id})
        
        elif action == 'save_continue':
            request.session['submission_id'] = submission.id
            return redirect('step4', submission_id=submission.id)

    context = {
        'submission': submission,
        'keywords': Keyword.objects.filter(submission=submission),
    }
    return render(request, 'step-3.html', context)

#Step-4
@login_required
def add_authors_institutions(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    # current_author = Author.objects.get(user=request.user)
    # to display author if logged in as admin
    # try:
    #     current_author = Author.objects.get(user=request.user)
    # except Author.DoesNotExist:
    #     current_author = None
    coauthor_form = CoAuthorForm()

    if request.method == "POST":
        if 'save_and_continue' in request.POST:
            request.session['submission_id'] = submission.id
            return redirect('step5', submission_id=submission.id)
            
    coauthors = CoAuthor.objects.filter(submission=submission)
    context = {
        'coauthor_form': coauthor_form,
        'submission': submission,
        'current_author': Author.objects.get(user=request.user),
        'coauthors': coauthors,
    }
    return render(request, 'step-4.html', context)

def add_coauthor_ajax(request, submission_id):
    if request.method == 'POST':
        form = CoAuthorForm(request.POST, submission=submission_id)
        if form.is_valid():
            coauthor = form.save(commit=False)
            coauthor.submission_id = submission_id
            coauthor.save()
            response = {
                'id': coauthor.id,
                'name': coauthor.name,
                'email': coauthor.email,
                'institution': coauthor.institution,
            }
            return JsonResponse(response, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

def remove_coauthor_ajax(request, submission_id):
    if request.method == 'POST':
        coauthor_id = request.POST.get('coauthor_id')
        CoAuthor.objects.filter(id=coauthor_id, submission_id=submission_id).delete()
        return JsonResponse({'id': coauthor_id}, status=200)

#Step-5
@login_required
def step5(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    try:
        funder = Funder.objects.get(submission=submission)
    except Funder.DoesNotExist:
        funder = None

    if request.method == "POST":
        form = SubmissionForm(request.POST, instance=submission)
        funder_form = FunderForm(request.POST, instance=funder)
        if form.is_valid() and (not submission.is_funded or (submission.is_funded and funder_form.is_valid())):
            form.save()

            if submission.is_funded:
                funder = funder_form.save(commit=False)
                funder.submission = submission
                funder.save()
            action = request.POST.get('action')
            if action == 'save_continue':
                return redirect('step6_review_submit', submission_id=submission.id)
            else:
                return render(request, 'step-5.html', {
                    'form': form,
                    'funder_form': funder_form,
                    'submission': submission,
                })
    else:
        form = SubmissionForm(instance=submission)
        funder_form = FunderForm(instance=funder)

    return render(request, 'step-5.html', {
        'form': form,
        'funder_form': funder_form,
        'submission': submission,
    })

#Step-6
@login_required
def step6_review_submit(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    submission_files = Submission_Files.objects.filter(submission=submission)
    keywords = Keyword.objects.filter(submission=submission)
    coauthors = CoAuthor.objects.filter(submission=submission)
    try:
        funder = Funder.objects.get(submission=submission)
    except Funder.DoesNotExist:
        funder = None

    empty_fields = []

    # Check each field and add to empty_fields if necessary
    if not submission.title:
        empty_fields.append('Title')
    if not submission.abstract:
        empty_fields.append('Abstract')
    if not submission.cover_letter:
        empty_fields.append('Cover Letter')
    if not submission.no_of_figures:
        empty_fields.append('Number of Figures')
    if not submission.no_of_tables:
        empty_fields.append('Number of Tables')
    if not submission.no_of_words:
        empty_fields.append('Number of Words')
    if not submission.coi_describe and submission.conflict_of_interest ==1  :
        empty_fields.append('Conflict of Interest Description')
    if not submission.category:
        empty_fields.append('Category')
    if not submission.journal:
        empty_fields.append('Journal')
    if not submission.article_type:
        empty_fields.append('Article Type')
    if not submission_files.exists():
        empty_fields.append('Submission Files')
    if not keywords.exists():
        empty_fields.append('Keywords')
    if not coauthors.exists():
        empty_fields.append('Co-Authors')
    if submission.is_funded == 1 and funder == None:
        empty_fields.append('Funder information')
    if submission.is_funded == 1 and submission.is_funded == 0:
        empty_fields.append(' is Funded')

    form = ReviewSubmitForm(initial={
            'title': submission.title,
            'abstract': submission.abstract,
            'cover_letter': submission.cover_letter,
            'is_funded': submission.is_funded,
            'figures': submission.no_of_figures,
            'tables': submission.no_of_tables,
            'words': submission.no_of_words,
            'is_submitted_already': submission.is_submitted_already,
            'acknowledgement_1': submission.acknowledgement_1,
            'acknowledgement_2': submission.acknowledgement_2,
            'acknowledgement_3': submission.acknowledgement_3,
            'conflict_of_interest': submission.conflict_of_interest,
            'coi_describe': submission.coi_describe,
            
        })

    context = {
        'form': form,
        'submission': submission,
        'category': submission.category,
        'journal': submission.journal,
        'Article_Type': submission.article_type,
        'submission_files': submission_files,
        'keywords': keywords,
        'coauthors': coauthors,
        'funder': funder,
        'empty_fields': empty_fields,

    }
    return render(request, 'step-6.html', context)


#**********************************************************************************************************************

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404, redirect, render
from django.http import FileResponse, HttpResponseBadRequest
from PyPDF2 import PdfWriter, PdfReader
from PIL import Image
import os
from .models import Submission, Submission_Files
from .forms import SubmissionFileForm
from docx2pdf import convert
from django.conf import settings
import logging
import pythoncom

logger = logging.getLogger(__name__)

#Step-2
@login_required
def submission_step_two(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    submission_files = Submission_Files.objects.filter(submission=submission)

    if request.method == 'POST':
        if 'remove_file' in request.POST:
            file_id = request.POST.get('file_id')
            file_to_remove = get_object_or_404(Submission_Files, id=file_id)
            file_to_remove.delete()
            return redirect('submission_step_two', submission_id=submission.id)
        else:
            form = SubmissionFileForm(request.POST, request.FILES, initial={'submission': submission})
            if form.is_valid():
                files = request.FILES.getlist('file')
                file_category = form.cleaned_data.get('file_category')

                for file in files:
                    file_size = file.size
                    Submission_Files.objects.create(
                        submission=submission,
                        file=file,
                        file_category=file_category,
                        file_size=file_size
                    )

                return redirect('submission_step_two', submission_id=submission.id)
    else:
        form = SubmissionFileForm(initial={'submission': submission})

    return render(request, 'step-2.html', {'form': form, 'submission': submission, 'submission_files': submission_files})

#View proof in Step-6
def view_proof(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    submission_files = Submission_Files.objects.filter(submission=submission)

    logger.debug(f"Attempting to process {len(submission_files)} files for submission ID: {submission_id}")

    try:
        merged_pdf_path = _process_files(submission_files)

        # Save the merged PDF to the final_file field of the Submission model
        submission.final_file.save(f'merged_submission_{submission.id}.pdf', open(merged_pdf_path, 'rb'))
        submission.save()

        # Optionally, delete the merged PDF from the file system if you don't need it anymore
        os.remove(merged_pdf_path)

        # Return the merged PDF as a response
        response = FileResponse(open(submission.final_file.path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="merged_submission_{submission.id}.pdf"'

        

        return response

    except Exception as e:
        logger.error(f"Error generating merged PDF for submission ID {submission_id}: {str(e)}")
        return HttpResponseBadRequest("An error occurred while generating the merged PDF. Please try again later.")

#File conversion and merging
def _process_files(files):
    pythoncom.CoInitialize()
    output_pdf_path = os.path.join(settings.MEDIA_ROOT, f'merged_submission.pdf')
    pdf_writer = PdfWriter()

    for file in files:
        file_extension = os.path.splitext(file.file.name)[1].lower()
        temp_path = default_storage.path(file.file.name)

        logger.debug(f"Processing file: {temp_path}")

        if not os.path.exists(temp_path):
            logger.error(f"File not found: {temp_path}")
            continue

        if file_extension == '.docx':
            temp_pdf_path = os.path.join(settings.MEDIA_ROOT, f"{os.path.splitext(file.file.name)[0]}.pdf")

            convert(temp_path, temp_pdf_path)  # Convert DOCX to PDF
            if os.path.exists(temp_pdf_path):
                with open(temp_pdf_path, 'rb') as pdf_file:
                    pdf_reader = PdfReader(pdf_file)
                    for page in pdf_reader.pages:
                        pdf_writer.add_page(page)

                default_storage.delete(temp_pdf_path)
            else:
                logger.error(f"Converted PDF not found: {temp_pdf_path}")

        elif file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
            temp_pdf_path = os.path.join(settings.MEDIA_ROOT, f"{os.path.splitext(os.path.basename(temp_path))[0]}.pdf")

            try:
                image = Image.open(temp_path)
                image.convert('RGB').save(temp_pdf_path)

                if os.path.exists(temp_pdf_path):
                    with open(temp_pdf_path, 'rb') as pdf_file:
                        pdf_reader = PdfReader(pdf_file)
                        for page in pdf_reader.pages:
                            pdf_writer.add_page(page)

                    default_storage.delete(temp_pdf_path)
                else:
                    logger.error(f"Converted PDF not found: {temp_pdf_path}")
            except Exception as e:
                logger.error(f"Error converting image to PDF: {e}")

        elif file_extension == '.pdf':
            if os.path.exists(temp_path):
                with open(temp_path, 'rb') as pdf_file:
                    pdf_reader = PdfReader(pdf_file)
                    for page in pdf_reader.pages:
                        pdf_writer.add_page(page)

                default_storage.delete(file.file.name)
            else:
                logger.error(f"PDF file not found: {temp_path}")

    with open(output_pdf_path, 'wb') as output_pdf_file:
        pdf_writer.write(output_pdf_file)

    logger.debug(f"Merged PDF saved at: {output_pdf_path}")
    return output_pdf_path

#Submit in Step-6
def submission_step_six(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    article_status_submitted = get_object_or_404(Article_Status, article_status='submitted')
    if request.method == 'POST':
        if 'action' in request.POST:
            if request.POST['action'] == 'submit':
                submission.article_status_id = article_status_submitted.id
                submission.save()

            # Redirect to a confirmation page or wherever needed
            return redirect('submitted')  # Replace 'confirmation_page' with your actual URL name
    return render(request, 'step-6.html', {'submission': submission})
