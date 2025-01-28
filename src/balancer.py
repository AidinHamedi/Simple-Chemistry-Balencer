# Libs >>>
from math import lcm

# Modules >>>


# Helpers >>>
def _atomic_composition(chemical_composition: list) -> dict:
    """Calculates the total number of atoms for each element in a chemical composition.

    Takes a list of chemical compounds and counts the total number of atoms for each
    unique element across all compounds in the composition.

    Args:
        chemical_composition (list): List of dictionaries containing chemical compounds with structure:
            [
                {
                    "decomposition": [{"element": str, "number": int}],
                    "chemical": str,
                    "multiplier": int
                }
            ]

    Returns:
        dict: Dictionary with element symbols as keys and their total atom count as values.
            Example: {"H": 2, "O": 1, "C": 1}

    Example:
        Input: [{"decomposition": [{"element": "H", "number": 2}, {"element": "O", "number": 1}]}]
        Output: {"H": 2, "O": 1}
    """
    # Make a var to keep track of the number of atoms of each element
    atomic_composition = {}

    # Iterate over the chemical composition
    for chemical in chemical_composition:
        # Get the number of atoms of each element
        for element in chemical["decomposition"]:
            # If the element is already in the atomic composition, add the number of atoms
            if element["element"] in atomic_composition:
                atomic_composition[element["element"]] += element["number"]
            else:
                atomic_composition[element["element"]] = element["number"]

    # Return the atomic composition
    return atomic_composition


def _atomic_lcm(
    reactants_composition: dict, products_composition: dict, raise_error: bool = True
) -> dict:
    """Calculates the least common multiple (LCM) of atom counts between reactants and products.

    Takes dictionaries of element counts from reactants and products and calculates the LCM
    for each element to help determine balanced equation coefficients.

    Args:
        reactants_composition (dict): Dictionary of element counts in reactants
            Example: {"H": 2, "O": 1}
        products_composition (dict): Dictionary of element counts in products
            Example: {"H": 2, "O": 1}
        raise_error (bool, optional): Whether to raise error if elements don't match. Defaults to True.

    Returns:
        dict: Dictionary with elements as keys and their LCM values as values
            Example: {"H": 2, "O": 1}

    Raises:
        SystemExit: If elements in reactants and products don't match and raise_error is True

    Example:
        Input:
            reactants = {"N": 2, "O": 2}
            products = {"N": 2, "O": 1}
        Output: {"N": 2, "O": 2}
    """
    # Check if all the elements in the reactants and products are the same
    if reactants_composition.keys() != products_composition.keys():
        if raise_error:
            raise SystemExit(
                "The elements in the reactants and products are not the same"
            )
        return {}

    # Make a var to hold the least common multiple
    atomic_lcms = {}

    # Find the least common multiple of the number of atoms of each element
    for element in reactants_composition:
        atomic_lcms[element] = lcm(
            reactants_composition[element], products_composition[element]
        )

    # Return the least common multiple
    return atomic_lcms


# Main >>>
def balance_formula(chemical_composition: dict) -> dict:
    # Get the reactants and products
    reactants = chemical_composition["reactants"]
    products = chemical_composition["products"]

    # Calculate the number of atoms of each element in the reactants and products
    reactants_composition = _atomic_composition(reactants)
    products_composition = _atomic_composition(products)

    # Find the least common multiple of the number of atoms of each element in the reactants and products
    atomic_lcms = _atomic_lcm(reactants_composition, products_composition)


print(
    balance_formula(
        {
            "reactants": [
                {
                    "decomposition": [{"element": "N", "number": 2}],
                    "chemical": "N2",
                    "multiplier": 1,
                },
                {
                    "decomposition": [{"element": "O", "number": 2}],
                    "chemical": "O2",
                    "multiplier": 1,
                },
            ],
            "products": [
                {
                    "decomposition": [
                        {"element": "N", "number": 2},
                        {"element": "O", "number": 1},
                    ],
                    "chemical": "N2O",
                    "multiplier": 1,
                }
            ],
        }
    )
)
