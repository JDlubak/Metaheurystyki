import sys

from file import configurate_parameters, read_solomon_data
from genetic_algorithm import GeneticAlgorithm
from ui import main_menu, menu_vrptw, see_details, see_results
from run_experiments import start_experiments


def choose_mode():
    is_first_call = True
    while True:
        mode = main_menu(is_first_call)
        is_first_call = False
        if mode in {'1', '2', '3'}:
            break
        elif mode == '4':
            see_details()
        elif mode == '5':
            print("Zakończenie programu.")
            sys.exit(0)
        else:
            print("Niepoprawny wybór. Spróbuj ponownie. ", end='')
    return mode


def main(params):
    crossing_probability = params[0]
    mutation_probability = params[1]
    population_size = params[2]
    iterations = params[3]
    crossing_method = params[4]
    selection_method = params[5]
    menu_vrptw(crossing_method, selection_method, crossing_probability,
               mutation_probability, population_size, iterations)
    try:
        choice = int(input("Twój wybór (1/2/3): "))
        catalog = 'solomon-100/In'
        if choice == 1:
            file = "r101.txt"
        elif choice == 2:
            file = "c101.txt"
        elif choice == 3:
            file = "rc101.txt"
        print(f"Wybrano: {file[:-4]}")
        data = read_solomon_data(f'{catalog}/{file}')
        number_of_clients = len(data['customers']) - 1
        ga = GeneticAlgorithm(population_size=population_size,
                              crossing_method=crossing_method,
                              selection_method=selection_method,
                              mutation_probability=mutation_probability,
                              crossing_probability=crossing_probability,
                              iterations=iterations,
                              number_of_clients=number_of_clients,
                              data=data,
                              instance_name=data['instance_name'])
        best, elapsed_time = ga.run()
        see_results(best, elapsed_time, data)
    except ValueError as e:
        print(f"Błąd: {e}")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")


if __name__ == "__main__":
    mode_choice = choose_mode()
    if mode_choice == '3':
        start_experiments()
    else:
        parameters = configurate_parameters(mode_choice)
        while True:
            main(parameters)
