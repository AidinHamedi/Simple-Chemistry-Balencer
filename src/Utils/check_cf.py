# Libs >>>
import re

# Modules >>>
from .element_symbols import ELEMENT_SYMBOLS

# Conf >>>
CHEMICAL_REGEX = re.compile(
    r'^'
    r'((?:[A-Z][a-z]?\d*|\((?:[A-Z][a-z]?\d*)+\)\d+)+'
    r'(?:\+(?:[A-Z][a-z]?\d*|\((?:[A-Z][a-z]?\d*)+\)\d+)+)*)'
    r'=>'
    r'((?:[A-Z][a-z]?\d*|\((?:[A-Z][a-z]?\d*)+\)\d+)+'
    r'(?:\+(?:[A-Z][a-z]?\d*|\((?:[A-Z][a-z]?\d*)+\)\d+)+)*)'
    r'$'
)

# Main >>>
def check_formula(formula: str, raise_error: bool = True) -> bool:
    """Checks if the given chemical formula is valid.
    
    Args:
        formula (str): The chemical formula to be checked.
        raise_error (bool, optional): If True, raises a SystemExit if the formula is invalid. Defaults to True.
    
    Returns:
        bool: True if the formula is valid, False otherwise."""
    # Check if the formula is valid
    if not re.match(CHEMICAL_REGEX, formula.strip(" ")):
        if raise_error:
            raise SystemExit("Invalid formula")
        return False

    # Return True if the formula is valid
    return True