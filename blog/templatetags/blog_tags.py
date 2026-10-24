from django import template
from ..models import Post, Comment
from django.db.models import Count
register = template.Library()


@register.simple_tag
def total_post():
    return Post.accepted.count()


@register.simple_tag
def total_comment():
    return Comment.objects.filter(active=True).count()


@register.simple_tag
def last_post_date():
    post = Post.accepted.order_by('-published_at').first()
    return post.published_at if post else None


# inclusion tag برای نمایش آخرین پست ها در قالب های دیگر استفاده می شود
@register.inclusion_tag('partials/last_posts.html')
# می توان با استفاده از id یا slug پست را از لیست حذف کرد
def latest_posts(count=3, exclude_slug=None):
    # استفاده از id سریع تر از slug میباشد اما slug برای انسان قابل فهم تر است
    last_posts = Post.accepted.order_by('-published_at')
    if exclude_slug:
        last_posts = last_posts.exclude(slug=exclude_slug)
    last_posts = last_posts[:count]
    return {'last_posts': last_posts}


@register.simple_tag
def most_popular_posts():
    popular_posts = Post.accepted.annotate(
        num_comments=Count('comments')).order_by('-num_comments')[:3]
    return popular_posts
