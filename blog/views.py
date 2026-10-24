# from multiprocessing import context
# from django.core.paginator import Paginator
#
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


# from django.core.paginator import Paginator

# from django.shortcuts import render
from django.template import context

from .models import Post
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, render, get_object_or_404
from .forms import CommentForm
from django.db.models import Q, query
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank, TrigramSimilarity


def index(request):
    return render(request, 'blog/index.html')


class PostListView(ListView):
    queryset = Post.accepted.all()
    paginate_by = 5
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'


def post_detail(request, slug):
    post = Post.accepted.get(slug=slug)
    form = CommentForm()
    comments = post.comments.filter(active=True)
    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, 'blog/post-detail.html', context)
# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/post-detail.html'
#     context_object_name = 'post'

#     def get_queryset(self):
#         return Post.accepted.all()


def post_comment(request, slug):
    """
    Handles the creation of comments for a specific post.
    Args:
        request: The HTTP request object.
        slug: The slug of the post for which the comment is being created.
    Returns:
        Renders the comment form template with the form and post context.
    """
    # تمام فرم های دارای foreign key به این صورت میباشد
    post = get_object_or_404(Post, status=Post.Status.ACCEPTED, slug=slug)
    # post = Post.accepted.get(slug=slug) این خط میتواند جایگزین خط بالا باشد
    if request.method == 'POST':

        form = CommentForm(data=request.POST)
        if form.is_valid():
            # commit زمانی استفاده میشود که فرم در دیتابیس ساخته شود اما سیو نه
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = CommentForm()
    comments = post.comments.filter(active=True)
    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, 'blog/post-detail.html', context)


# def post_search(request):
#     query = request.GET.get('q')
#     # config='english' برای جستجو در زبان انگلیسی استفاده میشود
#     query = SearchQuery(query, config='english', search_type='plain')
#     # title__icontains کیس insensitive و title__contains کیس sensitive میباشد
#     if not query:
#         return render(request, 'post_search.html', {'posts': [], 'q': query})
#     # posts = Post.accepted.filter(
#     #     # distinct() برای جلوگیری از تکراری شدن پست ها در صورت وجود در title و content استفاده میشود
#     #     title__icontains=query, content__icontains=query).distinct()
#     # reuslt_1 = Post.accepted.filter(title__icontains=query)
#     # reuslt_2 = Post.accepted.filter(content__icontains=query)
#     # posts = reuslt_1.union(reuslt_2)

#     # posts = Post.accepted.filter(
#     #     # دز صورت استفاده از Q باید از | برای or و & برای and استفاده شود همچنین میتوان از ~ برای not استفاده کرد
#     #     Q(title__search=query) | Q(content__search=query))
#     # posts = Post.accepted.annotate(search=SearchVector(title__search=query))
#     # weight A برای title و weight B برای content میباشد
#     vector = SearchVector('title', weight='A') + \
#         SearchVector('content', weight='B')

#     # posts = Post.accepted.annotate(search=vector).filter(
#     #     search=query).annotate(search=vector)
#     posts = Post.accepted.annotate(search=vector, rank=SearchRank(
#         vector, query)).filter(search=query).order_by('-rank')
#     context = {'posts': posts, 'q': query}
#     return render(request, 'blog/post_search.html', context)
def post_search(request):
    query = request.GET.get('q')
    posts = Post.accepted.none()
    if query:
        posts = Post.accepted.annotate(similarity=TrigramSimilarity('title', query)).filter(
            similarity__gt=0.3
        ).order_by('-similarity')
