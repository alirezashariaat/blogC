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
# from django.template import context

from django.db.models import query
from django.db.models.functions import Greatest

from .models import Post
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, render, get_object_or_404
from .forms import CommentForm
from django.db.models import Q, query, F
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
#     query = request.GET.get('q').strip()
#     if not query:
#         return render(request, 'post_search.html', {'posts': [], 'q': query})

#     search_query = SearchQuery(query, config='english', search_type='plain')
#     # config='english' برای جستجو در زبان انگلیسی استفاده میشود

#     vector = SearchVector('title', weight='A') + \
#         SearchVector('content', weight='B')

    # posts = Post.accepted.annotate(search=vector, rank=SearchRank(
    #     vector, search_query)).filter(search=search_query).order_by('-rank')
    # context = {'posts': posts, 'q': query}
    # return render(request, 'blog/post_search.html', context)
def post_search(request):
    search_text = request.GET.get('query', '').strip()
    posts = Post.accepted.none()
    if search_text:

        posts = (Post.accepted.annotate(title_similarity=TrigramSimilarity('title', search_text),
                                        content_similarity=TrigramSimilarity('content', search_text)).annotate(similarity=Greatest(F('title_similarity'), F('content_similarity'))))\
            .filter(Q(title__icontains=search_text) | Q(content__icontains=search_text) | Q(title_similarity__gt=0.05) | Q(content_similarity__gt=0.01)).order_by('-similarity')
    return render(request, 'blog/post_search.html', {'posts': posts, 'q': search_text})


# trigram search
    # res_1 = Post.accepted.annotate(similarity=TrigramSimilarity(
    #     'title', search_text)).filter(similarity__gt=0.1).order_by('-similarity')
    # res_2 = Post.accepted.annotate(similarity=TrigramSimilarity(
    #     'content', search_text)).filter(similarity__gt=0.1).order_by('-similarity')
    # posts = res_1 | res_2
    # context = {'posts': posts, 'q': search_text}
    # return render(request, 'blog/post_search.html', context)

# انواع مختلف جستجو در django
# 1. جستجو با استفاده از Q
# posts = Post.accepted.filter(
    #     # دز صورت استفاده از Q باید از | برای or و & برای and استفاده شود همچنین میتوان از ~ برای not استفاده کرد
    #     Q(title__search=query) | Q(content__search=query))
    # posts = Post.accepted.annotate(search=SearchVector(title__search=query))
    # weight A برای title و weight B برای content میباشد
# 2. جستجو با استفاده از SearchVector و SearchQuery

    #     vector = SearchVector('title', weight='A') + \
    #         SearchVector('content', weight='B')

    #     posts = Post.accepted.annotate(search=vector, rank=SearchRank(
    #         vector, search_query)).filter(search=search_query).order_by('-rank')
# 3. سرچ ساده
# posts = Post.accepted.filter(
    #     # distinct() برای جلوگیری از تکراری شدن پست ها در صورت وجود در title و content استفاده میشود
    #     title__icontains=query, content__icontains=query).distinct()
    # reuslt_1 = Post.accepted.filter(title__icontains=query)
    # reuslt_2 = Post.accepted.filter(content__icontains=query)
    # title__icontains کیس insensitive و title__contains کیس sensitive میباشد
    # posts = reuslt_1.union(reuslt_2)
    # posts = Post.accepted.annotate(search=vector).filter(
    #     search=query).annotate(search=vector)
