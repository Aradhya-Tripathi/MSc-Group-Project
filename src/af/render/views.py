from django.shortcuts import render


def plots(request):
    return render(request, "template.html")
