from django.shortcuts import render


def landing(request):
    return render(request, 'main/templates/index.html')


def dashboard(request):
    return render(request, 'user_panel/templates/index.html')


def tournament(request):
    return render(request, 'main/templates/tournament_tree.html')
