from z2.sa_algorithm import sa_algorithm
from z2.plot import draw_plots
from z2.print import get_parameters, print_analysis


def main():
    draw_plots()

    (func_id, epochs, number_of_attempts,
     temperature, alpha, k) = get_parameters()

    x, fx, solutions = sa_algorithm(func_id, epochs, temperature,
                                    alpha, number_of_attempts, k)

    print_analysis(x, fx, solutions)


while True:
    main()
