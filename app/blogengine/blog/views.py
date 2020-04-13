from django.core.paginator import Paginator
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Post, Tag
from .utils import *
from .forms import TagForm, PostForm


def get_form(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()
    page = Paginator(posts, 2).get_page(request.GET.get('page', 1))

    is_paginated = page.has_other_pages()
    prev_page_num = '?page={}'.format(page.previous_page_number()) if page.has_previous() else ''
    next_page_num = '?page={}'.format(page.next_page_number()) if page.has_next() else ''

    context = {
        'page': page,
        'is_paginated': is_paginated,
        'next_page': next_page_num,
        'prev_page': prev_page_num
    }
    return render(request, 'blog/index.html', context=context)


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    form_model = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDetailMixin, View):
    model = Post
    template = 'post_delete_form.html'
    redirect_url = 'posts_list_url'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    form_model = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, TagDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete_form.html'
    raise_exception = True


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = PostForm
    template = 'blog/post_create_form.html'
    redirect_url = 'tag_list_url'
    raise_exception = True


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})
