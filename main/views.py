from django.shortcuts import render

def show_main(request):
    context = {
        'name': 'Akhtar Eijaz Putranto',
        'class': 'PBP B'
    }

    return render(request, "main.html", context)
