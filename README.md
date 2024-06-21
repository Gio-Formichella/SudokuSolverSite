# Sudoku Solver Site

Sudoku puzzle solving Django web application. It allows users to:

* Manually enter Sudoku puzzles.
* Select variable choice strategies: Static order, Random, Minimum remaining values.
* Choose inference strategies: Maintaining arc consistency, Forward checking.
* Visualize the step-by-step solution process (optional).
* View information about the solving process (number of assignments, backtracks).

The primary goal of the project was to build a graphical interface for the backtracking sudoku solver I previously
implemented [here](https://github.com/Gio-Formichella/SudokuSolvers).
Additionally, it served as a hands-on learning experience of web applications and of the Django framework.

My interest in the world of CS lies in AI and not web development so excuse my spaghetti code and the minimalist
graphics.

## Dependencies

To install the packages needed to run the program you will need to run:

```
pip install -r requirements.txt
```

After the installments you are ready to run the server as default in Django.

## Usage

1. Run the Django development server:

```
python manage.py runserver
```

2. Access the application in your web browser (usually at http://127.0.0.1:8000/).

## Issues and Bugs

Please report any issues you encounter.
