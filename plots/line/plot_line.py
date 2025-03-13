import matplotlib.pyplot as plt

def plot(data, **kwargs):
    plt.plot(data['x'], data['y'], **kwargs)
    plt.title("line")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()