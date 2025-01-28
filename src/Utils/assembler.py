# Main >>>
def assemble_formula(chemical_composition: dict) -> str:
    """
    Assembles a chemical formula string from a dictionary of chemical components.

    The function takes a chemical composition dictionary and formats it into a readable
    chemical formula string with reactants and products separated by '=>'.

    Args:
        chemical_composition (dict): A dictionary containing two keys:
            - 'reactants': List of dictionaries with chemical components
            - 'products': List of dictionaries with chemical components
            Each component dictionary should have:
                - 'chemical': str - The chemical symbol/formula
                - 'multiplier': int - The coefficient for the chemical

    Returns:
        str: A formatted chemical formula string (e.g. "H2+O2=>H2O")

    Examples:
        >>> composition = {
        ...     'reactants': [
        ...         {'chemical': 'H2', 'multiplier': 1},
        ...         {'chemical': 'O2', 'multiplier': 1}
        ...     ],
        ...     'products': [
        ...         {'chemical': 'H2O', 'multiplier': 2}
        ...     ]
        ... }
        >>> assemble_formula(composition)
        'H2+O2=>H2O'
    """
    # Make a var to hold the formula
    formula = ""

    # Iterate over the formula scopes
    for chemical_scope, scope_chemicals in chemical_composition.items():
        # Iterate over the chemicals in the scope
        for chemical in scope_chemicals:
            # Add the chemical to the formula
            if chemical["multiplier"] > 1:
                formula += f"({chemical['chemical']}){chemical['multiplier']}"
            else:
                formula += chemical["chemical"]
            # Add the + sign if it's not the last chemical
            if chemical != scope_chemicals[-1]:
                formula += "+"
        # Add the => sign for the next scope (products)
        if chemical_scope == "reactants":
            formula += "=>"

    # Return the formula
    return formula
