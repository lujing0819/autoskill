import sympy as sp
from sympy import integrate, sympify
import sys

def calculate_definite_integral():
    if len(sys.argv) != 5:
        print("Usage: python script.py <function_expression> <lower_bound> <upper_bound> <output_file>")
        return
    
    function_expr = sys.argv[1]
    lower_bound = float(sys.argv[2])
    upper_bound = float(sys.argv[3])
    output_file = sys.argv[4]
    
    x = sp.Symbol('x')
    
    try:
        func = sympify(function_expr)
        result = integrate(func, (x, lower_bound, upper_bound))
        
        with open(output_file, 'w') as f:
            f.write(f"Function: {function_expr}\n")
            f.write(f"Integration bounds: [{lower_bound}, {upper_bound}]\n")
            f.write(f"Definite integral result: {result}\n")
            f.write(f"Numerical value: {float(result)}\n")
        
        print(f"Result saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    calculate_definite_integral()