# from multiprocessing import context
# from django.core.paginator import Paginator
#
# from django.shortcuts import render
# from .models import Post
#
#
# def post_list(request):
#     posts = Post.accepted.all()
#     paginator = Paginator(posts, 2)
#     page_number = request.GET.get('page', 1)
#     posts = paginator.page(page_number)
#
#     return render(request, 'blog/post_list.html', {'posts': posts})
#
#
# def post_detail(request, slug):
#     post = Post.accepted.get(slug=slug)
#     context = {'post': post}
#     return render(request, 'blog/post-detail.html', context)

from django.core.paginator import Paginator

from django.shortcuts import render
from .models import Post
from django.views.generic import ListView,DetailView

class PostListView(ListView):
    queryset = Post.accepted.all()
    paginate_by = 3
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post-detail.html'
    context_object_name = 'post'
    def get_queryset(self):
        return Post.accepted.all()
