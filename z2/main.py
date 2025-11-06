from z2.sa_algorithm import sa_algorithm
from z2.plot import draw_plots
from z2.print import get_parameters, print_analysis

draw_plots()
first_run = True
while True:
    if first_run:
        (func_id, epochs, number_of_attempts,
         temperature, alpha, k) = get_parameters()

    if not first_run:
        response = input("Czy chcesz zmienić parametry? (t)")
        if response == "t":
            (func_id, epochs, number_of_attempts,
             temperature, alpha, k) = get_parameters()

    x, fx, solutions, time = sa_algorithm(func_id, epochs, temperature,
                                    alpha, number_of_attempts, k)

    print_analysis(x, fx, solutions, time)
    first_run = False
