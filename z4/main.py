from itertools import product
from ACO import run_algorithm, create_distance_matrix
from file import load_config, read_file

print("Select how algorithm should be run:")
print("1 - Use values from config and draw plot")
print("2 - Run experiments for various values and save them to files")

choice = input("Twój wybór (1/2): ").strip()
if choice == "1":
    (file, p_random, alpha, beta,
     iterations, rho, col_size) = (load_config())
    df = read_file(file)
    dm = create_distance_matrix(df)
    run_algorithm(file, dm, df, p_random, alpha, beta,
                  iterations, rho, col_size, plot=True)
elif choice == "2":
    files = ["A-n80-k10.txt"]
    p_randoms = [0]
    alphas = [2]
    betas = [5]
    iterations = [200]
    rhos = [0.3]
    col_sizes = [100]

    for file in files:
        df = read_file(file)
        dm = create_distance_matrix(df)
        for p_random, alpha, beta, iteration, rho, col_size in (
                product(p_randoms, alphas, betas,
                        iterations, rhos, col_sizes)):
            for _ in range(20):
                run_algorithm(file, dm, df, p_random, alpha, beta,
                              iteration, rho, col_size)
else:
    print("Wrong.")
