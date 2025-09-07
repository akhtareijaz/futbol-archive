from django.shortcuts import render

def show_main(request):
    context = {
        'nama_aplikasi' : 'Futbol Archive',
        'npm' : '2406495571',
        'name': 'Akhtar Eijaz Putranto',
        'class': 'PBP B'
    }

    return render(request, "main.html", context)
