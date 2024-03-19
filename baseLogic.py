import numpy as np
import matplotlib.pyplot as plt

def generate_data(equation, std_dev, num_points, bounds=None):
    def func(x):
        return eval(equation)
    
    # gen x values
    if bounds:
        x_values = np.linspace(bounds[0][0], bounds[1][0], num_points)
    else:
        x_values = np.linspace(-10, 10, num_points)  # default bounds
    
    # calc y vals and add noise
    y_values = [func(x) for x in x_values]
    noise = np.random.normal(0, std_dev, num_points)
    y_noisy = y_values + noise
    
    return x_values, y_noisy

equation = 'ln(x)'  # x ** 2  
std_dev = 0.1    # noise standard deviation
num_points = 100   
bounds = [(0.3,0.3), (10.5,10.5)]  # Optional bounds for x and y like [(1, 1), (10, 100)]

x_data, y_data = generate_data(equation, std_dev, num_points, bounds)

plt.scatter(x_data, y_data, label='Data Points')
plt.plot(x_data, [eval(equation) for x in x_data], color='red', label='Input Equation')

# export x and y values to one txt 
data = np.column_stack((x_data, y_data))
np.savetxt('data.txt', data, fmt='%.2f')

plt.legend()
plt.show()
