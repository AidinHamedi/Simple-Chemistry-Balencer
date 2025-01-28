# Libs >>>

# Modules >>>
from .Utils.check_cf import check_formula
from .decomposer import decompose_formula

# Conf >>>

# Prep >>>

# Main >>>
def chem_balance(formula: str = None) -> dict:
    # Check if a formula is given
    if formula is None:
        formula = input("Formula: ")

    # Check if the formula is valid
    if not check_formula(formula, raise_error=False):
        return {"Error": "An invalid formula is given!"}
    
    # Decompose the formula
    decomposed_formula = decompose_formula(formula)
