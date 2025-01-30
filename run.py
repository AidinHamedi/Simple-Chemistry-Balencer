# Modules >>>
from src.Utils.assembler import assemble_formula
from src.Utils.check_cf import check_formula
from src.decomposer import decompose_formula
from src.balancer import balance_formula


# Main >>>
def chem_balance():
    # Get the formula
    formula = input("Formula: ")

    # Remove spaces
    formula = formula.replace(" ", "")

    # Check if the formula is valid
    check_formula(formula, raise_error=True)

    # Decompose the formula
    decomposed_formula = decompose_formula(formula)

    # Balance the formula
    balanced_formula = balance_formula(decomposed_formula)

    # Assemble the balanced formula
    balanced_formula_str = assemble_formula(balanced_formula)

    # Print the balanced formula
    print(balanced_formula_str)


# Start >>>
if __name__ == "__main__":
    chem_balance()