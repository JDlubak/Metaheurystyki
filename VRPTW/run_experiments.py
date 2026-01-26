from itertools import product
from concurrent.futures import ProcessPoolExecutor, as_completed
from genetic_algorithm import GeneticAlgorithm
from file import read_solomon_data


def run_single(params):
    (data, iters, pop, cp, mp, sel, cross, task_id) = params
    try:
        number_of_clients = len(data['customers']) - 1
        ga = GeneticAlgorithm(
            population_size=pop,
            crossing_method=cross,
            selection_method=sel,
            mutation_probability=mp,
            crossing_probability=cp,
            iterations=iters,
            number_of_clients=number_of_clients,
            data=data,
            instance_name=data['instance_name']
        )

        ga.run(print_result=False, task_id=task_id)
        return (f"Sukces: Zadanie {task_id} | Plik: "
                f"{data['instance_name']} | P:{pop}, I:{iters}, "
                f"CP:{cp}, MP:{mp}, S:{sel}, C:{cross}")
    except Exception as e:
        return f"Błąd w zadaniu {task_id}: {e}"


def start_experiments():
    files = ["r101.txt", "c101.txt", "rc101.txt"]
    iters = [100, 300, 1000]
    populations = [40, 100, 200]
    cps = [0.6, 0.8, 1.0]
    mps = [0.05, 0.1, 0.2]
    selections = ["ranking", "tournament"]
    crossings = ["single", "double"]
    tasks = []
    task_id = 1
    print("Rozpoczynam przygotowywać zadania...")

    for file in files:
        data = read_solomon_data(f'solomon-100/In/{file}')
        for combination in product(iters, populations, cps,
                                   mps, selections, crossings):
            for _ in range(5):
                i, p, cp, mp, s, c = combination
                tasks.append((data, i, p, cp, mp, s, c, task_id))
                task_id += 1

    total_tasks = len(tasks)
    print(f"Przygotowano {total_tasks} zadań... Uruchamiam!")

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(run_single, t) for t in tasks]
        completed = 0
        for future in as_completed(futures):
            completed += 1
            print(f"[{completed}/{total_tasks}] {future.result()}")

    print("\n--- WSZYSTKIE EKSPERYMENTY ZAKOŃCZONE ---")


if __name__ == "__main__":
    start_experiments()




