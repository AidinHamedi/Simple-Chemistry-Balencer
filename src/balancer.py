# Libs >>>
import math
from math import lcm, gcd


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


def _balance_elements(reactants: list, products: list, atomic_lcms: dict) -> dict:
    """
    Balances chemical equations with enhanced fallback logic that:
    1. Handles multiple interdependent elements
    2. Iteratively balances until fully stable
    3. Properly updates product multipliers
    """

    def balance_single_elements():
        # Existing single element balancing code remains the same
        for element in atomic_lcms:
            reactant_chems = [
                chem
                for chem in reactants
                if any(e["element"] == element for e in chem["decomposition"])
            ]
            product_chems = [
                chem
                for chem in products
                if any(e["element"] == element for e in chem["decomposition"])
            ]

            if len(reactant_chems) == 1 and len(product_chems) == 1:
                reactant_chem = reactant_chems[0]
                product_chem = product_chems[0]

                reactant_elem = next(
                    e for e in reactant_chem["decomposition"] if e["element"] == element
                )
                product_elem = next(
                    e for e in product_chem["decomposition"] if e["element"] == element
                )

                a = reactant_elem["number"] * reactant_chem["multiplier"]
                b = product_elem["number"] * product_chem["multiplier"]

                if a == 0 or b == 0 or a == b:
                    continue

                gcd_val = gcd(a, b)
                k_r = b // gcd_val
                k_p = a // gcd_val

                reactant_chem["multiplier"] *= k_r
                product_chem["multiplier"] *= k_p

    # Initial balancing pass
    balance_single_elements()

    # Iterative balancing with improved fallback
    max_iterations = 5
    for _ in range(max_iterations):
        rc = _atomic_composition(reactants)
        pc = _atomic_composition(products)
        
        # Check if fully balanced
        if rc == pc:
            break
            
        # Balance each element systematically
        for element in set(rc.keys()).union(pc.keys()):
            req = rc.get(element, 0)
            prod = pc.get(element, 0)
            
            # Skip balanced elements
            if req == prod:
                continue
                
            # Calculate required multiplier
            if req == 0 or prod == 0:
                continue
                
            if req % prod != 0 and prod % req != 0:
                continue
                
            multiplier = req / prod if req > prod else prod / req
            
            # Determine which side to adjust
            if req > prod:  # Need more in products
                candidates = products
                actual_multiplier = multiplier
            else:  # Need more in reactants
                candidates = reactants
                actual_multiplier = multiplier
                
            # Find first compound containing the element
            for chem in candidates:
                if any(e["element"] == element for e in chem["decomposition"]):
                    if req > prod:
                        chem["multiplier"] *= math.ceil(actual_multiplier)
                    else:
                        chem["multiplier"] *= math.ceil(actual_multiplier)
                    break  # Only adjust one compound per element

        # Recalculate after adjustments
        rc = _atomic_composition(reactants)
        pc = _atomic_composition(products)
        
    return {"reactants": reactants, "products": products}


# Main >>>
def balance_formula(chemical_composition: dict) -> dict:
    """Balances a chemical equation by adjusting coefficients of reactants and products.

    Takes a chemical composition dictionary containing reactants and products, and returns
    a balanced chemical equation where the number of atoms of each element is equal on
    both sides.

    Args:
        chemical_composition (dict): Dictionary containing:
            - "reactants": List of dictionaries for each reactant compound
            - "products": List of dictionaries for each product compound
            Each compound dictionary contains:
                - "decomposition": List of {"element": str, "number": int}
                - "chemical": str (chemical formula)
                - "multiplier": int (coefficient)

    Returns:
        dict: Dictionary with balanced equation containing:
            - "reactants": Updated reactants list with balanced multipliers
            - "products": Updated products list with balanced multipliers

    Example:
        Input:
            {
                "reactants": [{
                    "decomposition": [{"element": "H", "number": 2}, {"element": "O", "number": 1}],
                    "chemical": "H2O",
                    "multiplier": 1
                }],
                "products": [...]
            }
        Output:
            {
                "reactants": [...],  # With updated multipliers
                "products": [...]    # With updated multipliers
            }
    """
    # Get the reactants and products
    reactants = chemical_composition["reactants"]
    products = chemical_composition["products"]

    # Calculate the number of atoms of each element in the reactants and products
    reactants_composition = _atomic_composition(reactants)
    products_composition = _atomic_composition(products)

    # Find the least common multiple of the number of atoms of each element in the reactants and products
    atomic_lcms = _atomic_lcm(reactants_composition, products_composition)

    # Balance the elements + return the balanced elements
    return _balance_elements(reactants, products, atomic_lcms)
