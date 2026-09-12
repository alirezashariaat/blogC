from multiprocessing import context

from django.shortcuts import render
from .models import Post
def post_list(request):
    posts = Post.accepted.all()
    return render(request, 'blog/post_list.html',{'posts':posts})
def post_detail(request, slug):
    post = Post.accepted.get(slug=slug)
    context = {'post': post}
    return render(request, 'blog/post-detail.html',context)

