import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

categories = ['categ 1', 'categ  2', 'categ  3', 'categ  4']
values = [3, 7, 2, 5]

plt.bar(categories, values, color='blue')

plt.xlabel('categ ')
plt.ylabel('values')
plt.title('Test Figure')

plt.show()

# test for understanding jupyter working with git
