import matplotlib.pyplot as plt
from rpy2.robjects import pandas2ri
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

def plot(data, **kwargs):
    print("plot")
    pandas2ri.activate()
    ggplot2 = importr('ggplot2')
    df = pandas2ri.py2rpy_pandasdataframe(data)
    
    robjects.r('''
    library(ggplot2)
    p <- ggplot(df, aes(x = x, y = y)) + 
         geom_line(color = %(color)s) +
         ggtitle("Line Plot")
    print(p)
    ''', color=kwargs.get('color', 'blue'))
    print("done")