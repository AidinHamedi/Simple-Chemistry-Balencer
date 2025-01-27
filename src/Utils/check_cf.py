# Libs >>>
import re

# Conf >>>
FORMULA_REGEX = r""

# Main >>>
def check_formula(formula: str, raise_error: bool = False) -> bool:
    # Check if the formula is valid
    if not re.match(FORMULA_REGEX, formula):
        if raise_error:
            raise ValueError("Invalid formula") from None
        return False
    
    # Return True if the formula is valid
    return True