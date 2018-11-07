from django.shortcuts import render

from blog import models, forms


def blog(request):
    context = {'posts': models.Post.objects.all()}
    return render(request, 'blog.html', context)


def view_post(request):
    pass
