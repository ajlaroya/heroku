from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin # class based 'decorator'
from django.urls import reverse_lazy
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm

# BLOG VIEWS
class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    # python sql query
    def get_queryset(self):
        # filter post model by descending (-) published date
        # __lte = field lookup
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the posts
        context['detailed'] = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:5]
        return context

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list') # redirect until after deletion

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = "blog/post_list.html"
    template_name = 'blog/post_draft.html' # fixed my draft view problem!
    model = Post

    def get_queryset(self):
        # query published dates with no date
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


# COMMENT VIEWS
@login_required  # requires login to run function
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

# @login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk) # gets post or returns a 404
    if request.method == 'POST': # if form is filled and submitted
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # don't save yet
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk) # primary key of blog post
    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk # save post pk so can be used after deletion
    comment.delete()
    return redirect('post_detail',pk=post_pk)
