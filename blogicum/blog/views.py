from django.shortcuts import render, get_object_or_404

from blog.models import Post, Category

from datetime import datetime


def index(request):
    post_list = Post.objects.filter(
        pub_date__lt=datetime.now(),
        is_published=True,
        category__is_published=True
    ).order_by('created_at')[0:5]
    context = {
        'post_list': post_list
    }
    template = 'blog/index.html'
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects,
        slug=category_slug,
        is_published=True
    )
    post_list = Post.objects.select_related('category').filter(
        pub_date__lt=datetime.now(),
        category__is_published=True,
        category__slug=category_slug,
        is_published=True
    )

    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)


def post_detail(request, pk):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related('category').order_by('category'),
        pk=pk,
        is_published=True,
        category__is_published=True,
        pub_date__lt=datetime.now()
    )
    context = {
        'post': post
    }
    return render(request, template, context)
