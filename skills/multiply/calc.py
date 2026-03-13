import sys

def multiply_and_save(num1, num2, filename):
    result = num1 * num2
    with open(filename, 'w') as f:
        f.write(str(result))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <num1> <num2> <filename>")
        sys.exit(1)
    
    num1 = float(sys.argv[1])
    num2 = float(sys.argv[2])
    filename = sys.argv[3]
    
    multiply_and_save(num1, num2, filename)
    print(f"Result {num1} * {num2} = {num1 * num2} saved to {filename}")