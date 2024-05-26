from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("solver/", views.solve_sudoku_puzzle, name="solver"),
    path("details/", views.detail, name="details")
]
