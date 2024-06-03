from django.shortcuts import render


# Create your views here.
def solve_sudoku_puzzle(request, puzzle: list):
    solved = False
    while not solved:
        assignments = []  # TODO: check board variable assignments
        context = {
            "assignments": assignments
        }
        return render(request, "sudoku_solver/home", context)


def detail(request):
    context = {
        "name": "Gio"
    }
    return render(request, "sudoku_solver/details.html", context)


def home(request):
    return render(request, "sudoku_solver/home.html")


def sudoku_board(request):
    return render(request, "sudoku_solver/sudoku_board.html", {})
