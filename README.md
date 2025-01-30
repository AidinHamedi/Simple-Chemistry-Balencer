# Simple Chemistry Balancer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

The **Simple Chemistry Balancer** is an open-source Python project designed to balance chemical equations. It provides users with the ability to input unbalanced chemical formulas and receive balanced versions as output.

### Key Features:

- Input validation for chemical formulas.
- Decomposition of complex compounds into their elements.
- Calculation of coefficients needed to balance chemical reactions.
- Assembly of balanced equations in a readable format.

## 📂 Project Structure

The project is organized within the `aidinhamedi-simple-chemistry-balencer` directory, which contains several key files and folders:

```
└── aidinhamedi-simple-chemistry-balencer/
    ├── README.md
    ├── LICENSE
    ├── pyproject.toml
    ├── run.py
    ├── .python-version
    └── src/
        ├── __init__.py
        ├── balancer.py
        ├── decomposer.py
        └── Utils/
            ├── __init__.py
            ├── assembler.py
            ├── check_cf.py
            └── element_symbols.py
```

### File Descriptions

- **README.md**: Provides an overview, installation instructions, usage guide, and licensing information. 📄

- **LICENSE**: Specifies the project is licensed under the MIT License. 📜

- **pyproject.toml**: Contains metadata about the project such as name, version, dependencies, etc. 💾

- **run.py**: The entry point for running the application. It handles user input and orchestrates other modules to balance chemical equations. 🔧

- **.python-version**: Specifies the Python version used in this project (Python 3.13). 🐍

- **src/**: Contains all source code files organized into subdirectories:
  - `__init__.py`: Initializes package imports.
  - `balancer.py`: Implements functions for balancing chemical formulas.
  - `decomposer.py`: Provides functionality to decompose input formulas into elements and compounds.
  - **Utils/**: A utility directory with helper modules:
    - `assembler.py`: Assembles balanced equations from component data structures.
    - `check_cf.py`: Validates the format of input chemical formulas using regular expressions.
    - `element_symbols.py`: Lists all known element symbols for validation purposes.

## 🚀 Installation and Usage

### Installation Steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AidinHamedi/Simple-Chemistry-Balencer.git
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd Simple-Chemistry-Balencer
   ```

3. **Run the Script**: Ensure you have Python 3.9 or higher installed, then execute:
   ```bash
   python run.py
   ```

### Usage:

Upon running `run.py`, users will be prompted to enter a chemical equation in the format `Reactants=>Products`. For example:

```
Formula: H2+O2=>H2O
```

The program processes this input, balances it by calculating appropriate coefficients for each compound, and outputs the balanced equation. Using the above input as an example, the output would be:

```
H2+O2=>(H2O)2
```

## 🤔 How It Works

1. **Input Validation**: The `check_cf.py` module validates that the user’s input follows a recognized format for chemical formulas.

2. **Decomposition**: Using `decomposer.py`, each compound in the formula is broken down into its elemental constituents along with their respective counts and multipliers, especially handling nested structures like parentheses.

3. **Balancing**: The `balancer.py` module calculates coefficients that balance both sides of a chemical equation by ensuring equal numbers of atoms for each element on either side.

4. **Assembly**: Finally, the balanced components are assembled into a human-readable string format using `assembler.py`.

## 📝 License

This project is licensed under the MIT License, allowing users to freely use, modify, and distribute it with proper attribution. 🌟
