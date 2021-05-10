from django.shortcuts import render , get_object_or_404
from django.views.generic import ListView, DetailView, CreateView ,UpdateView ,DeleteView
from django.contrib.auth.models import User
from .models import Post,Category,Comment
from django.contrib.auth.mixins import LoginRequiredMixin ,  UserPassesTestMixin
from .forms import PostForm ,AddCommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse ,reverse_lazy
# Create your views here.


from django.http import HttpResponse

posts =[
    {
        'author':'shahil',
        'title':'blog post',
        'content':'first post',
        'date_posted':'27/11/18'
    },
    {
        'author': 'shahil j',
        'title': 'blog post 1',
        'content': 'post 2',
        'date_posted': '27/11/19'
    }
]


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    # app/model_viewtype.html
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostListView,self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


class UserPostListView(ListView):
    model = Post
    # app/model_viewtype.html
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


def categoryview(request,cats):
    category_posts = Post.objects.filter(category=cats)
    return render(request,'blog/category.html',{'cats':cats,'category_posts':category_posts})


def likeview(request,pk):
    post = get_object_or_404(Post,id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('post-detail',args=[str(pk)]))

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostDetailView,self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post,id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["cat_menu"] = cat_menu
        context["total_likes"] = total_likes
        context['liked'] = liked
        return context



class AddCommentView(LoginRequiredMixin,CreateView):
    model = Comment
    form_class = AddCommentForm
    template_name = 'blog/add_comments.html'
    #fields = '__all__'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']

        return super().form_valid(form)

    success_url = reverse_lazy('blog-home')



class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    form_class = PostForm
    #fields = ['title', 'content','category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    form_class = PostForm
    #fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

