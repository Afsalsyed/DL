
# views.py
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
import logging
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from .forms import UserRegistrationForm
from .models import Author, User,Editor
from django.contrib.auth.forms import SetPasswordForm
import logging
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from oss.models import Journal, Journal_Editor_Assignment
from django.template.loader import render_to_string
from django.contrib.auth.forms import SetPasswordForm     #set_new_password
from django.db import IntegrityError                      #register
from django.contrib.auth import views as auth_views       #CustomPasswordResetConfirmView
from django.contrib.auth.forms import PasswordResetForm   #CustomPasswordResetConfirmView
from django.contrib.auth.forms import PasswordResetForm   #password_reset_view
from django.contrib.auth.views import PasswordChangeView  #CustomPasswordChangeView
from django.urls import reverse_lazy                      #CustomPasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin 
import json

logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('user_management')  # Redirect to user_management.html
                else:
                    return redirect('startnew')  # Or another view for regular users
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@require_GET
def fetch_groups(request):
    username = request.GET.get('username')
    user = User.objects.get(username=username)
    groups = Group.objects.all()
    user_groups = user.groups.values_list('id', flat=True)
    groups_data = [{'id': group.id, 'name': group.name} for group in groups]
    return JsonResponse({'groups': groups_data, 'user_groups': list(user_groups)})


@csrf_exempt
@require_POST
def update_user_groups(request):
    username = request.POST.get('username')
    groups = request.POST.getlist('groups[]')
    user = get_object_or_404(User, username=username)
    user.groups.clear()
    for group_id in groups:
        group = get_object_or_404(Group, id=group_id)
        user.groups.add(group)
    return JsonResponse({'status': 'success'})

logger = logging.getLogger(__name__)

def reset_user_password(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            new_password = request.POST['new_password']
            email = request.POST['email']
            
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()

            # Send email
            subject = 'Your password has been reset'
            message = f'Hello {username},\n\nYour new password is: {new_password}\n\nPlease log in and change it to something more secure.'
            from_email = 'mitung62@gmail.com'
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)

            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

def search_users(request):
    query = request.GET.get('query', '')
    users = User.objects.filter(first_name__icontains=query) | User.objects.filter(username__icontains=query)
    users_data = list(users.values('first_name', 'last_name', 'username', 'email', 'is_superuser'))

    journal_usernames = list(User.objects.filter(groups__name__in=['AE', 'AIC']).values_list('username', flat=True))
    return JsonResponse({'users': users_data, 'journal_usernames': journal_usernames})


def generate_token(user):
    return default_token_generator.make_token(user)

def encode_uid(user):
    return urlsafe_base64_encode(force_bytes(user.pk))

def decode_uid(uid):
    return force_str(urlsafe_base64_decode(uid))

def registration_complete(request):
    return render(request, 'registration_complete.html')

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        logger.error(f'User does not exist or token is invalid: uidb64={uidb64}, token={token}')
    
    if user is not None and default_token_generator.check_token(user, token):
        return redirect('set_new_password', uidb64=uidb64, token=token)
    else:
        logger.error(f'Token verification failed: uidb64={uidb64}, token={token}')
        return render(request, 'email_verification_failed.html')



def send_verification_email(user):
    token = generate_token(user)
    uid = encode_uid(user)
    verification_link = f"{settings.SITE_URL}{reverse('set_new_password', kwargs={'uidb64': uid, 'token': token})}"
    
    subject = 'Verify your email'
    message = f"""
    Dear {user.username},
    
    Please verify your email by clicking the link below:
    {verification_link}
    
    
    Thank you.
    """
    
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])




@login_required
def home(request):
    return render(request, 'home.html')







@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        is_active = request.POST.get('is_active') == 'true'

        if not email:
            return JsonResponse({'success': False, 'error': 'Email is required'})

        username = email  # Set the username as the email

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=User.objects.make_random_password(),  # Generate a random password
                is_active=is_active
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def user_management(request):
    users = User.objects.all()
    
    journal_usernames = list(User.objects.filter(groups__name__in=['AE', 'AIC']).values_list('username', flat=True))
    context = {
        'users': users,
        'journal_usernames': json.dumps(journal_usernames),  # Convert list to JSON string
        'journals' : Journal.objects.all()
    }
    return render(request, 'user_management.html', context)

# views.py

def get_journals(request):
    username = request.GET.get('username')
    editor = Editor.objects.filter(user__username=username).first()
    
    journals = Journal.objects.all()
    assigned_journal = Journal_Editor_Assignment.objects.filter(editor=editor).first()
    
    data = {
        'journals': list(journals.values('id', 'title')),
        'selected_journal': assigned_journal.journal.id if assigned_journal else None
    }
    
    return JsonResponse(data)

def assign_journal(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        journal_id = request.POST.get('journal_id')

        if not username or not journal_id:
            return JsonResponse({'success': False, 'error': 'Username or Journal ID is missing.'})

        try:
            # Get the User object based on the username
            user = get_object_or_404(User, username=username)

            # Get the Journal object based on the journal_id
            journal = get_object_or_404(Journal, id=journal_id)

            # Get or create the Editor object associated with the User
            editor, created = Editor.objects.get_or_create(user=user)

            # Remove existing journal assignments for the editor
            Journal_Editor_Assignment.objects.filter(editor=editor).delete()

            # Assign the selected journal to the editor
            Journal_Editor_Assignment.objects.create(journal=journal, editor=editor)

            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User does not exist.'})
        except Journal.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Journal does not exist.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.username = form.cleaned_data.get('email')
                user.is_active = False
                
                user.save()
                user.refresh_from_db()
                author = Author(
                    user=user,
                    title=form.cleaned_data.get('title'),
                    institution=form.cleaned_data.get('institution'),
                    address=form.cleaned_data.get('address'),
                    city=form.cleaned_data.get('city'),
                    state=form.cleaned_data.get('state'),
                    country=form.cleaned_data.get('country'),
                    mobile_no=form.cleaned_data.get('mobile_no'),
                    zipcode=form.cleaned_data.get('zipcode'),
                    orcid_id=form.cleaned_data.get('orcid_id'),
                    scopus_id=form.cleaned_data.get('scopus_id'),
                )
                author.save()
                
                send_verification_email(user)
                return redirect('registration_complete')
            except IntegrityError:
                form.add_error('email', 'This email address is already registered.')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def set_new_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if request.method == 'POST' and user is not None and default_token_generator.check_token(user, token):
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            user.is_active = True  # Ensure the user is active
            user.save()
            logger.info(f'Password successfully set for user: {user.username}')
            return redirect('login')
        else:
            logger.error(f'Form errors: {form.errors}')
    else:
        form = SetPasswordForm(user)
        if user is None:
            logger.error(f'User is None, uidb64: {uidb64}, token: {token}')
        if not default_token_generator.check_token(user, token):
            logger.error(f'Token verification failed, uidb64: {uidb64}, token: {token}')

    context = {
        'form': form,
        'uidb64': uidb64,
        'token': token,
    }

    if uidb64:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=uid)
            context['username'] = user.first_name
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            context['username'] = None

    return render(request, 'set_new_password.html', context)

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        uidb64 = self.kwargs.get('uidb64')
        if uidb64:
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = get_object_or_404(User, pk=uid)
                context['username'] = user.first_name
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                context['username'] = None
                
        
        return context


def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                form.add_error('email', 'Email address not found.')
                return render(request, 'password_reset_form.html', {'form': form})

            form.save(request=request)
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()

    return render(request, 'password_reset_form.html', {'form': form})

def profile(request):
    return render(request, 'profile.html')


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('password_change_done')


#**************logout****************

def custom_logout(request):
    logout(request)
    return redirect('login')



#*************************************************

from dl.models import Published_article, Issue

def index_view(request):
    journals = Journal.objects.all()  # Fetch all journal entries
    return render(request, 'index.html', {'journals': journals})

def current_issue_view(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    # Fetch the latest published submission for the journal
    issue = Issue.objects.filter(volume__journal=journal).order_by('-id')
    latest_issues = Published_article.objects.filter(issue__in= issue).order_by('-id')
    print(latest_issues)
    return render(request, 'current_issue.html', {'journal': journal, 'latest_issues': latest_issues})
    