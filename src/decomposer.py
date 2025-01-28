# Libs >>>
import re
from contextlib import suppress

# Modules >>>
from Utils.element_symbols import ELEMENT_SYMBOLS

# Helpers >>>
def _split_chemicals(formula: str) -> list:
    # Split the chemicals with '+' sign
    return formula.split("+")

def _split_elements(chemical: str, raise_error: bool = True) -> list:
    """Splits a chemical formula into its constituent elements and their quantities.
    
    This function parses chemical formulas including nested structures with parentheses
    and handles multiple-digit coefficients. It processes the formula character by character
    and tracks element levels for nested structures.

    Flow:
    1. Initializes tracking variables (elements list, nesting level, multipliers stack)
    2. Iterates through the chemical formula character by character
    3. Handles special cases:
        - Opening bracket '(' : increases nesting level
        - Closing bracket ')' : decreases level and processes multiplier
        - Element symbols: identifies single/double letter elements
        - Numbers: processes as multipliers for elements
    4. Applies stack multipliers to handle nested structures
    
    Examples:
        "(NH4)2Cr2O7" -> [
            {'element': 'N', 'multiplier': 2},
            {'element': 'H', 'multiplier': 8},
            {'element': 'Cr', 'multiplier': 2},
            {'element': 'O', 'multiplier': 7}
        ]

    Args:
        chemical (str): The chemical formula to parse (e.g., "H2O", "(NH4)2SO4")
        raise_error (bool, optional): If True, raises SystemExit for invalid elements. 
                                    Defaults to True.

    Returns:
        list: List of dictionaries containing elements and their quantities.
              Each dictionary has keys:
              - 'element': str (element symbol)
              - 'multiplier': int (quantity of the element)

    Raises:
        SystemExit: If raise_error is True and an invalid element symbol is encountered
    """
    # Make vars to keep track of the elements num etc...
    elements = []
    element_level = 0
    stack_multipliers = [1]
    
    # Make the loop counter
    idx = 0
    
    # Iterate over the chemical
    while idx < len(chemical):
        # Get the char
        char = chemical[idx]
        # If the char is a left bracket
        if char == "(":
            # Increase the element level
            element_level += 1
            # skip
            idx += 1
            continue
        # If the char is a right bracket
        elif char == ")":
            # Decrease the element level
            element_level -= 1
            # Get the multiplier
            s_multiplier = 1
            with suppress(IndexError):
                if chemical[idx + 1].isdigit():
                    s_multiplier = int(chemical[idx + 1])
                    idx += 1
            stack_multipliers.append(s_multiplier)
            # skip
            idx += 1
            continue
        # Get the element symbol
        element_symbol = char
        with suppress(IndexError):
            if all((chemical[idx + 1].isalpha(), chemical[idx + 1].islower())):
                element_symbol += chemical[idx + 1]
                idx += 1
        # Check if the element symbol is in the element symbols
        if element_symbol not in ELEMENT_SYMBOLS:
            if raise_error:
                raise SystemExit(f"Invalid element symbol: {element_symbol}")
            return []
        # Check if the next char is a digit or not
        if chemical[idx + 1].isalpha():
            element_multiplier = 1
        else:
            # Increase the index
            idx += 1
            # Get the char
            char = chemical[idx]
            # Get the element multiplier
            element_multiplier = char
            with suppress(IndexError):
                while chemical[idx + 1].isdigit():
                    element_multiplier += chemical[idx + 1]
                    idx += 1
            element_multiplier = int(element_multiplier)
        # Add the element to the elements list
        elements.append({"element": element_symbol, "multiplier": element_multiplier, "level": element_level})
        # Increase the index
        idx += 1
    # Handle the stack multipliers
    for element in elements:
        element["multiplier"] *= stack_multipliers[element["level"]]
        del element["level"]

    # Return the elements
    return elements

# Main >>>
def decompose_formula(formula: str) -> dict:
    # Split the formula into the reactants and products
    reactants, products = formula.split("=>")
    
    
    
    
