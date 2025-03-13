import matplotlib.pyplot as plt

def plot(data, **kwargs):
    plt.bar(data['x'], data['y'], **kwargs)
    plt.title("Bar Plot")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()