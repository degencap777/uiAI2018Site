from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from blog import models, forms


def blog(request):
    context = {'posts': models.Post.objects.all()}
    return render(request, 'blog.html', context)


def view_post(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    context = {'post': post}
    comment_form = forms.CommentForm()
    if request.user.is_authenticated:
        comment_form.initial = {'full_name': request.user.get_full_name(), 'email': request.user.email}
    if request.method == 'POST':
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            models.Comment.objects.create(
                full_name=comment_form.cleaned_data.get('full_name'),
                email=comment_form.cleaned_data.get('email'),
                text=comment_form.cleaned_data.get('text'),
                post=post,
            )
            messages.success(request, 'نظر شما پس از تایید قابل مشاهده خواهد بود.')
            return redirect(reverse('view_post', kwargs={'pk': pk}))
        else:
            messages.error(request, 'لطفاً اشکالات فرم را برطرف کنید.')
    context['comment_form'] = comment_form
    return render(request, 'post.html', context)
