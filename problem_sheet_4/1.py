import re

def construct_symbol_table(source_code):
    symbol_table = {}

    # Extract variable declarations
    # pattern explanation:
    '''
    \b matches a word boundary
    \w matches a word character
    \s matches a whitespace character
    * matches 0 or more of the preceding token
    ? matches 0 or 1 of the preceding token
    . matches any character except a newline
    (?:) matches the pattern inside the parentheses but does not capture it
    \b(w+) matches a word boundary followed by 1 or more word characters
    \s* matches 0 or more whitespace characters'''
    variable_pattern = r'\b(\w+)\s*:\s*(\w+)\s*=\s*(.*?)(?:\n|$)'
    variables = re.findall(variable_pattern, source_code)
    for variable in variables:
        name, datatype, value = variable
        symbol_table[name] = {
            'datatype': datatype,
            'bytes_allocated': 4,
            'initial_value': value
        }

    # Extract function declarations
    function_pattern = r'\bdef\s+(\w+)\s*\((.*?)\)\s*->\s*(\w+):'
    functions = re.findall(function_pattern, source_code)
    for function in functions:
        name, parameters, return_type = function
        symbol_table[name] = {
            'parameters': parameters.split(','),
            'return_type': return_type
        }

    return symbol_table
    
def main():
    source_code = """
        def add(x: int, y: int) -> int:
            return x + y

        def subtract(x: int, y: int) -> int:
            return x - y

        def multiply(x: int, y: int) -> int:
            return x * y

        def divide(x: int, y: int) -> int:
            return x / y

        def main():
            x: int = 5
            y: int = 10
            z: int = add(x, y)
            print(z)
    """

    symbol_table = construct_symbol_table(source_code)
    for name, attributes in symbol_table.items():
        print(f"Name: {name}")
        for key, value in attributes.items():
            print(f"\t{key}: {value}")

if __name__ == '__main__':
    main()

    