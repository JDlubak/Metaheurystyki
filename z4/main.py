from file import load_config
from ACO import run_algorithm
from itertools import product

plot = input("Do you want to run algorithm using values from config "
             "file and plot the result path afterwards?\n"
             "If so, provide any input, otherwise press enter.\n"
             "If you press enter, algorithm will start 5 times for "
             "every single one of possible 3072 combinations, and\n"
             "results from these 15360 experiments would be saved to "
             "files.")
if plot:
    (file, p_random, alpha, beta,
     iterations, rho, col_size) = (load_config())
    run_algorithm(file, p_random, alpha, beta,
                  iterations, rho, col_size, plot)
else:
    files = ["A-n32-k5.txt", "A-n80-k10.txt"]
    p_randoms = [0, 0.01, 0.05, 0.1]
    alphas = [0.5, 1, 2, 5]
    betas = [1, 2, 5, 10]
    iterations = [100, 500, 1000]
    rhos = [0.1, 0.3, 0.5, 0.8]
    col_sizes = [10, 20, 50, 100]
    for file, p_random, alpha, beta, iteration, rho, col_size in (
            product(files, p_randoms, alphas, betas,
                    iterations, rhos, col_sizes)):
        run_algorithm(file, p_random, alpha, beta,
                      iteration, rho, col_size)
