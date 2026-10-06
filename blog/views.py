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

# from django.core.paginator import Paginator

# from django.shortcuts import render
from .models import Post, Comment
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .forms import CommentForm
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


@require_POST
def post_comment(request, post_slug):  
    post = get_object_or_404(Post,status = Post.Status.ACCEPTED,slug = post_slug)

    # post = Post.accepted.filter(slug=post_slug) این خط میتواند جایگزین خط بالا باشد
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)#commit زمانی استفاده میشود که
