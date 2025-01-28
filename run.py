# Modules >>>
from src.main import chem_balance


# Main >>>
def main():
    # Get the formula from the user
    formula = input("Formula: ")

    # Balance the formula
    balanced_formula = chem_balance(formula)

    # Debug
    print(balanced_formula)


# Start >>>
if __name__ == "__main__":
    main()
