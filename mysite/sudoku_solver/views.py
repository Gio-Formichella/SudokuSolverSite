from django.shortcuts import render


# Create your views here.
def detail(request):
    context = {
        "name": "Gio"
    }
    return render(request, "sudoku_solver/details.html", context)


def home(request):
    return render(request, "sudoku_solver/home.html")
