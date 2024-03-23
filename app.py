from sympy import symbols, sympify
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import pandas as pd

app = Flask(__name__)
x_data = None
y_data = None

def generate_data(equation, std_dev, num_points, bounds=None):
    x = symbols('x')
    transformations = (standard_transformations + (implicit_multiplication_application,))
    
    equation = equation.replace('^', '**').replace('ln', 'log')
    equation_sympy = parse_expr(equation, transformations=transformations)
    
    def func(x_val):
        return float(equation_sympy.subs(x, x_val))
    
    if bounds:
        x_values = np.linspace(bounds[0][0], bounds[1][0], num_points)
    else:
        x_values = np.linspace(-10, 10, num_points)  
    
    y_values = [func(x) for x in x_values]
    noise = np.random.normal(0, std_dev, num_points)
    y_noisy = y_values + noise
    
    return x_values, y_noisy

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        equation = request.form['equation']
        std_dev = float(request.form['std_dev'])
        num_points = int(request.form['num_points'])
        bounds = [(float(request.form['x_min']), 0), 
                  (float(request.form['x_max']), 0)]
        
        try:
            x_data, y_data = generate_data(equation, std_dev, num_points, bounds)
        except:
            return jsonify({'error': 'Invalid equation'})

        data = np.column_stack((x_data, y_data))
        np.savetxt('data.txt', data, fmt='%.2f')
        
        df = pd.read_csv('data.txt', delimiter=' ')
        df.to_csv('data.csv', index=False)
        return jsonify({'x_data': x_data.tolist(), 'y_data': y_data.tolist()})
    
    return render_template('index.html')

@app.route('/export-csv')
def export_csv():
    try:
        with open('data.csv', 'r') as file:
            data = file.read()
        return data
    except FileNotFoundError:
        return "No data available", 404

@app.route('/export-txt')
def export_txt():
    try:
        with open('data.txt', 'r') as file:
            data = file.read()
        return data
    except FileNotFoundError:
        return "No data available", 404

if __name__ == '__main__':
    app.run(debug=True)
