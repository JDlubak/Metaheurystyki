from file import load_config
from ACO import run_algorithm
from itertools import product

print("Select how algorithm should be run:")
print("1 - Use values from config and draw plot")
print("2 - Run experiments for various values and save them to files")

choice = input("Twój wybór (1/2): ").strip()
if choice == "1":
    (file, p_random, alpha, beta,
     iterations, rho, col_size) = (load_config())
    run_algorithm(file, p_random, alpha, beta,
                  iterations, rho, col_size, plot=True)
elif choice == "2":
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
        for _ in range(5):
            run_algorithm(file, p_random, alpha, beta,
                          iteration, rho, col_size)
else:
    print("Wrong.")
