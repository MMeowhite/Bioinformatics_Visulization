import matplotlib.pyplot as plt

def plot(data, **kwargs):
    plt.scatter(data['x'], data['y'], **kwargs)
    plt.title("Scatter Plot")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()