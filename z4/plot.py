import matplotlib.pyplot as plt
import numpy as np

def draw_route(df, order, shortest):
    x = df.iloc[order]["x"].values
    y = df.iloc[order]["y"].values

    plt.figure(figsize=(8, 8))
    plt.plot(np.append(x, x[0]), np.append(y, y[0]), '-o', color='blue')
    for i, (xi, yi) in enumerate(zip(x, y)):
        if i < len(df):
            plt.text(xi, yi, str(i+1), fontsize=12, color='red')

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Wykres trasy")
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(8, 8))
    x3 = df["x"].values
    y3 = df["y"].values
    plt.scatter(x3, y3)
    for i, (xi, yi) in enumerate(zip(x3, y3)):
        plt.text(xi, yi, str(i), fontsize=12)
    plt.show()
    print(shortest)

