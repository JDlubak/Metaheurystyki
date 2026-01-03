def beale_function(x: float, y: float) -> float:
    term1 = (1.5 - x + x * y)**2
    term2 = (2.25 - x + x * y**2)**2
    term3 = (2.625 - x + x * y**3)**2
    return term1 + term2 + term3

def himmelblaus_function(x: float, y: float) -> float:
    term1 = (x**2 + y - 11)**2
    term2 = (x + y**2 - 7)**2
    return term1 + term2

FUNCTIONS = {
    1: {
        "name": "Beale Function",
        "func": beale_function,
        "range": (-4.5, 4.5)
    },
    2: {
        "name": "Himmelblau's Function",
        "func": himmelblaus_function,
        "range": (-5, 5)
    }
}

def load_function_config(func_id: int) -> dict:
    if func_id not in FUNCTIONS:
        raise ValueError(f"Niepoprawny wybór funkcji. Dostępne ID: {list(FUNCTIONS.keys())}")
    return FUNCTIONS[func_id]