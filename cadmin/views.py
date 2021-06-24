from django.shortcuts import render, redirect, get_object_or_404, reverse, Http404
from blog.forms import PostForm
from blog.models import Post, Author, Category, Tag
from django.contrib import messages
from django.conf import settings
from blog.urls import urlpatterns
from . forms import UserRegisterForm, ProfileUpdatForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from mysite import helpers
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.db import IntegrityError
# Create your views here.
def register(request):
    if request.method == 'POST':

        form = UserRegisterForm(request.POST)
        if form.is_valid():
            activation_key = helpers.generate_activation_key(username = request.POST['username'])
            subject = 'Django Blog Account Activation'
            message = f'''\n
            please click on the link below to activate your account: \n
            {request.scheme}://{request.get_host()}/cadmin/activate/account/?key={activation_key}
            '''
            error = False
            try:

                send_mail(subject, message, settings.SERVER_EMAIL, [request.POST['email']])
                messages.success(request,f'Account created! Click on the link sent to your email to activate the account')
            except:
                error = True
                messages.success(request,'Unable to send email. Please try again')
            
            if not error:
                u = User.objects.create_user(request.POST['username'],
                                            request.POST['email'],
                                            request.POST['password1'],
                                            is_active = 0)
                author = Author()
                author.activation_key = activation_key
                author.user = u
                author.save()

            
            return redirect('cadmin:login')
    else:
        form = UserRegisterForm()
    return render(request, 'cadmin/register.html', {'form':form})


def activate_account(request):
    key = request.GET['key']
    if not key:
        raise Http404()

    r = get_object_or_404(Author, activation_key=key, email_validated=False)
    r.user.is_active = True
    r.user.save()
    r.email_validated = True
    r.save()

    return render(request, 'cadmin/activated.html')

    
@login_required
def profile(request):
    if request.method == 'POST':
        
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdatForm(request.POST,
                                    request.FILES,
                                    instance=request.user.author)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile Updated!')
            return redirect(reverse('cadmin:profile'))

    else:
        if request.user.is_staff:
            return render(request, 'cadmin/profile.html')
        else:

            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdatForm(instance=request.user.author)
        

            context = {
                        'u_form':u_form,
                        'p_form':p_form
                        }
            return render(request, 'cadmin/profile.html',context)


