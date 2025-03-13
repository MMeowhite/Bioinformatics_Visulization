import seaborn as sns
import matplotlib.pyplot as plt

def plot(data, **kwargs):
    penguins = sns.load_dataset("penguins")

    g = sns.histplot(data=penguins,
                     x="flipper_length_mm",
                     hue="species",
                     multiple="stack")
    sns.set(style='whitegrid', font_scale=1.2)
    plt.show()