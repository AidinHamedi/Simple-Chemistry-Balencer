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
    print(balanced_formula)
    # Assemble the balanced formula
    balanced_formula_str = assemble_formula(balanced_formula)

    # Print the balanced formula
    print(balanced_formula_str)


# Start >>>
if __name__ == "__main__":
    chem_balance()

{
    "reactants": [
        {
            "decomposition": [
                {"element": "Al", "number": 1},
                {"element": "O", "number": 3},
                {"element": "H", "number": 3},
            ],
            "chemical": "Al(OH)3",
            "multiplier": 2,
        },
        {
            "decomposition": [
                {"element": "H", "number": 2},
                {"element": "S", "number": 1},
                {"element": "O", "number": 4},
            ],
            "chemical": "H2SO4",
            "multiplier": 3,
        },
    ],
    "products": [
        {
            "decomposition": [
                {"element": "Al", "number": 2},
                {"element": "S", "number": 3},
                {"element": "O", "number": 12},
            ],
            "chemical": "Al2(SO4)3",
            "multiplier": 1,
        },
        {
            "decomposition": [
                {"element": "H", "number": 2},
                {"element": "O", "number": 1},
            ],
            "chemical": "H2O",
            "multiplier": 1,
        },
    ],
}
