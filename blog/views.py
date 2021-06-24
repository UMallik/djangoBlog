from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post, Category, Tag, Author
from . forms import FeedbackForm
from django.contrib import messages
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from mysite import helpers
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.db import IntegrityError


# def post_list(request):
#     post = Post.objects.all().order_by('-pub_date')
#     # pagintator = Paginator(post, 3)
#     return render(request, 'blog/index.html',{'posts':post})

##LisView for post list
class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    ordering = ['-pub_date']
    paginate_by = 5

# def post_detail(request, pk, slug):
#     post = get_object_or_404(Post, pk=pk)
#     # post = Post.objects.get(pk=pk)
#     return render(request, 'blog/post_detail.html',{'post':post})

#PostDetailView
class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

def post_by_category(request, slug):
    # category = get_object_or_404(Category, slug = slug)
    category = Category.objects.get(slug = slug)
    # post = get_list_or_404(Post.objects.order_by('-pub_date'), category__slug = slug)
    post = Post.objects.filter(category__slug = slug)

    context = {
        'category': category,
        'posts': post
    }

    return render(request, 'blog/post_by_category.html', context)

def post_by_tag(request, slug):
    # tag = get_object_or_404(Tag, slug = slug)
    tag = Tag.objects.get(slug = slug)
    # post = get_list_or_404(Post.objects.order_by('-pub_date'), tags__slug = slug)
    post = Post.objects.filter(tags__slug = slug)

    context = {
        'tag':tag,
        'posts': post
    }

    return render(request, 'blog/post_by_tag.html', context)

def test_redirect(request):
    return HttpResponseRedirect('https://www.google.com')

def feedback(request):
    if request.method == 'POST':
        f = FeedbackForm(request.POST)
        if f.is_valid():
            f.save()
            message = messages.add_message(request, messages.INFO, 'Feedback Submitted')
            
            return redirect('blog:feedback')

    else:
        f = FeedbackForm()
    return render(request, 'blog/feedback.html', {'form':f})




# @login_required
# def post_add(request):
#     if request.method == 'POST':
#         # creating a bound form with form data
#         f = PostForm(request.POST) 

#         if f.is_valid():
#             f.save()
#             messages.add_message(request, messages.SUCCESS,'Post Added!')
#             return redirect('cadmin:post_add')
#     else:
#         # show unbound form to user
#         f = PostForm()

#         return render(request, 'cadmin/post_add.html',{'form':f})




class PostCreateView(LoginRequiredMixin, CreateView):

    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content','category','tags']
    def form_valid(self,form):
        form.instance.author = Author.objects.get(user = self.request.user)
        return super().form_valid(form)



# @login_required
# def post_update(request, pk):
#     post = get_object_or_404(Post, pk = pk)

#     if request.method == 'POST':
#         f = PostForm(request.POST, instance=post)
#         if f.is_valid():
#             f.save()
#             messages.add_message(request, messages.INFO,'Post Updated!')
#             return redirect(reverse('cadmin:post_update', args=[post.pk]))
#     else:
#         f = PostForm(instance=post)
#         return render(request,'cadmin/post_update.html', {'form':f,'post':post})

#PostUpdateView
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content','category','tags']
    def form_valid(self,form):
        form.instance.author = Author.objects.get(user = self.request.user)
        return super().form_valid(form)

    def test_func(self):
        post  = self.get_object()
        a = Author.objects.get(user = self.request.user)
        
        if a == post.author:

            return True
        return False


#PostDeleteView
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'
    def test_func(self):
        post  = self.get_object()
        a = Author.objects.get(user = self.request.user)
        
        if a == post.author:
            return True
        return False


#users posts

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'
    ordering = ['-pub_date'] #does not get called when we use get_queryset method
    paginate_by = 1

    def get_queryset(self):
        
        a = Author.objects.get(user = self.request.user)
        return Post.objects.filter(author = a).order_by('-pub_date')


#Category Create

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'blog/category_form.html'
    fields = ['name']
    def form_valid(self,form):
        form.instance.author = Author.objects.get(user = self.request.user)
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError:
            messages.add_message(request, messages.ERROR,
                                'You already have registered a Category with this name. ' + \
                                'All of your Category names must be unique.')
            return render(request, template_name=self.template_name, context=self.get_context_data())

#User Categories
class UserCategoryView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'blog/user_category.html'
    context_object_name = 'category'

    def get_queryset(self):
        a = Author.objects.get(user = self.request.user)
        return Category.objects.filter(author = a)

#Tag Create

class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    template_name = 'blog/tag_form.html'
    fields = ['name',]

    def form_valid(self, form):
        form.instance.author = Author.objects.get(user = self.request.user)
        return super().form_valid(form)

    def post(self,request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError:
            messages.error(request, 'Tag Already Exists')
            return render(request, template_name = self.template_name, context = self.get_context_data())

# # User Tags

class UserTagView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'blog/user_tag.html'
    context_object_name = 'tag'
    
    def get_queryset(self):
        author = Author.objects.get(user = self.request.user)
        return Tag.objects.filter(author = author)


def track_user(request):
    response = render(request, 'blog/track_user.html')
    if not request.COOKIES.get('visits'):
        response.set_cookie('visits', 1, 3600*24*365*2)
    else:
        visits = int(request.COOKIES.get('visits', '1')) + 1
        response.set_cookie('visits', str(visits),3600*24*365*2)
    return response


def stop_tracking(request):
    if request.COOKIES.get('visits'):
        response = HttpResponse('Cookies Cleared')
        response.delete_cookie('visits')
    else:
        response = HttpResponse('We are not tracking you')

    return response


def test_session(request):
    request.session.set_test_cookie()
    return HttpResponse('Testing session cookie')

def test_delete(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        response = HttpResponse('Worked')
    else:
        response = HttpResponse("did not work")

    return response

def save_session_data(request):
    # set new data
    request.session['id'] = 1
    request.session['name'] = 'root'
    request.session['password'] = 'rootpass'
    return HttpResponse("Session Data Saved")


def access_session_data(request):
    response = ""
    if request.session.get('id'):
        response += "Id : {0} <br>".format(request.session.get('id'))
    if request.session.get('name'):
        response += "Name : {0} <br>".format(request.session.get('name'))
    if request.session.get('password'):
        response += "Password : {0} <br>".format(request.session.get('password'))

    if not response:
        return HttpResponse("No session data")
    else:
        return HttpResponse(response)


def delete_session_data(request):
    try:
        del request.session['id']
        del request.session['name']
        del request.session['password']
    except KeyError:
        pass

    return HttpResponse("Session Data cleared")





