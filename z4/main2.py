from itertools import product
from concurrent.futures import ProcessPoolExecutor, as_completed
from ACO import run_algorithm, create_distance_matrix
from file import read_file

def run_single(params):
    (task_id, file, dm, df,
     p_random, alpha, beta,
     iteration, rho, col_size) = params
    run_algorithm(
        file, dm, df,
        p_random, alpha, beta,
        iteration, rho, col_size,
        task_id
    )
    return (file, p_random, alpha, beta, iteration, rho, col_size)

if __name__ == "__main__":
    files = ["A-n32-k5.txt", "A-n80-k10.txt"]
    p_randoms = [0.01, 0.05, 0.1]
    alphas = [0.5, 2, 5]
    betas = [1, 3, 6]
    iterations = [100, 300, 600]
    rhos = [0.1, 0.3, 0.7]
    col_sizes = [15, 40, 80]

    tasks = []
    task_id = 1

    for file in files:
        df = read_file(file)
        dm = create_distance_matrix(df)
        for combination in product(p_randoms, alphas, betas, iterations, rhos, col_sizes):
            p_random, alpha, beta, iteration, rho, col_size = combination
            for _ in range(5):
                tasks.append((
                    task_id, 
                    file, dm, df,
                    p_random, alpha, beta,
                    iteration, rho, col_size
                ))
                task_id += 1

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(run_single, task) for task in tasks]
        for future in as_completed(futures):
            result = future.result()
            print(f"Finished: {result}")
