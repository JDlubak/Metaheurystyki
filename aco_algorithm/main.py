from itertools import product
from ACO import run_algorithm, create_distance_matrix
from file import load_config, read_file

print("Select how algorithm should be run:")
print("1 - Use values from config and draw plot")
print("2 - Run experiments for various values and save them to files")

choice = input("Your choice (1/2): ").strip()
if choice == "1":
    (file, p_random, alpha, beta,
     iterations, rho, col_size) = (load_config())
    df = read_file(file)
    dm = create_distance_matrix(df)
    run_algorithm(file, dm, df, p_random, alpha, beta,
                  iterations, rho, col_size, plot=True)
elif choice == "2":
    files = ["A-n32-k5.txt", "A-n80-k10.txt"]
    p_randoms = [0.01, 0.05, 0.1]
    alphas = [0.5, 2, 5]
    betas = [1, 3, 6]
    iterations = [100, 300, 600]
    rhos = [0.1, 0.3, 0.7]
    col_sizes = [15, 40, 80]
    for file in files:
        df = read_file(file)
        dm = create_distance_matrix(df)
        for p_random, alpha, beta, iteration, rho, col_size in (
                product(p_randoms, alphas, betas,
                        iterations, rhos, col_sizes)):
            for _ in range(5):
                run_algorithm(file, dm, df, p_random, alpha, beta,
                              iteration, rho, col_size)
else:
    print("Wrong.")
