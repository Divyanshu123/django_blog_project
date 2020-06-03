from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse,reverse_lazy
from django.utils import timezone
from django.http import HttpResponse,HttpResponseRedirect
from .models import Post,Comment
from .forms import PostForm,CommentForm,RegisterForm,UserLoginForm
from django.views.generic import TemplateView,CreateView,UpdateView,DeleteView,ListView,DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms


class IndexView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class AboutPage(TemplateView):
    template_name = 'blog/about.html'

class AfterRegister(TemplateView):
    template_name = 'blog/after_register.html'


def after_login(request,pk):
    user = get_object_or_404(User,pk=pk)
    return render(request,'blog/after_login.html',{'user':user})


class ContactPage(TemplateView):
    template_name = 'blog/contact.html'


def author_posts(request,pk):
    author = get_object_or_404(User,pk=pk)
    author_posts = author.posts.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request,'blog/author_posts.html',{'author_posts':author_posts,'author':author})


def delete_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:author_posts',pk=post.author.pk)

    else:
        return render(request,'blog/post_confirm_delete.html',{'post':post})



class UpdatePost(UpdateView):
    redirect_field_name = 'post_detail.html'
    model = Post
    form_class = PostForm

    template_name = 'blog/update_post.html'







class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post_detail'
    template_name = 'post_detail.html'


def post_comments(request,pk):
    post = get_object_or_404(Post,pk=pk)
    comments = post.comments.all().order_by('created_date')
    return render(request,'blog/post_comments.html',{'post':post,'comments':comments})








@login_required
def write_post(request,pk):
    user = get_object_or_404(User,pk=pk)
    post_form = PostForm()
    if request.method == 'POST':

        post_form = PostForm(request.POST)


        if post_form.is_valid():
            post_form = post_form.save(commit=False)
            post_form.author = user
            post_form.save()

            return redirect('blog:author_posts',pk=pk)

        else:
            return HttpResponse('Invalid Credential!')

    return render(request,'blog/user_write_post.html',{'post_form':post_form,'user':user})
#


# class CreatePost(LoginRequiredMixin,CreateView):
#
#
#     login_url = '/'
#     redirect_field_name = '/'
#
#     form_class = PostForm
#     template_name='blog/user_write_post.html'
#
#     model = Post





def register(request):
    registered = False
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)

        if user_form.is_valid():
            form = user_form.save()
            form.set_password(form.password)
            form.save()
            registered = True
            return redirect('/after_register/')

        else:
            return HttpResponse('Invalid Credentials!')

    else:
        form = RegisterForm()

    return render(request,'blog/register.html',{'registered':registered,'form':form})




def user_login(request):
    user_login_form = UserLoginForm()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return redirect('blog:after_login',pk = user.id)

            else:
                return HttpResponse('user is not active!')

        else:
            return HttpResponse('invalid User Credentials!')

    return render(request,'blog/login.html',{'user_login_form':user_login_form})


@login_required
def user_logout(request):
    logout(request)
    return render(request,'blog/logout.html',)



def write_comment(request,pk):
    post = get_object_or_404(Post,pk=pk)
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        author = request.POST['author']
        text = request.POST['text']
        if comment_form.is_valid():
            comment_form.save()
            a = post.comments.create(author=author,text=text)
            a.save()
            return redirect('blog:post_detail', pk=pk)

        else:
            HttpResponse("Invalid Inputs!")

    return render(request,'blog/write_comment.html',{'comment_form':comment_form})


# def save_draft(request,pk):
#     user = get_object_or_404(User,pk=pk)
#     post = user.posts.filter(published_date__isnull=True).last()
#     if post is not None:
#         post.save()
#         return redirect('blog:author_posts',pk=pk)
#     else:
#         return redirect('blog:author_posts',pk=pk)



def user_drafts(request,pk):
    user = get_object_or_404(User,pk=pk)
    drafts = user.posts.filter(published_date__gt=timezone.now()).order_by('created_date')
    return render(request,'blog/user_drafts.html',{'user':user,'drafts':drafts})

def user_draft_detail(request,pk):
    draft = get_object_or_404(Post,pk=pk)
    return render(request,'blog/user_draft_detail.html',{'draft':draft})


def publish_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('blog:author_posts',pk=post.author.pk)
