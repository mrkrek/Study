from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.models import User
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostList(ListView):
    model = Post
    ordering = 'author'
    template_name = 'posts.html'
    context_object_name = 'id'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news_2.html'
    context_object_name = 'id_news_2'


class PostCreate(LoginRequiredMixin, CreateView, View):
    login_url = '/accounts/login/'
    form_class = PostForm
    model = Post
    template_name = 'create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_info = 'статья', 'новость'
        return super().form_valid(form)


def create_post(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news/')

    return render(request, 'create.html', {'form': form})


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'update.html'
    success_url = reverse_lazy('post_list')

    class ProtectedView(LoginRequiredMixin, TemplateView):
        template_name = 'signup.html'

    def form_valid(self, form):
        post = form.cleaned_data
        form.save(post)
        return super(PostUpdate, self).form_valid(form)


class PostDelete(DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('post_list')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/login/'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('news/signin/')


class MyView(PermissionRequiredMixin, View):
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')


class AddPost(PermissionRequiredMixin, CreateView):
    permission_required = ('news',)
