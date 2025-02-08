from collections import deque
from typing import Callable, List, Tuple


class CSP(object):
    """
    Represents a Constraint Satisfaction Problem (CSP).
    Attributes:
        variables (dict): A dictionary that maps variables to their domains.
        constraints (list): A list of constraints in the form of [constraint_func, variables].
        unassigned_var (list): A list of unassigned variables.
        var_constraints (dict): A dictionary that maps variables to their associated constraints.

    Methods:
        add_constraint(constraint_func, variables): Adds a constraint to the CSP.
        add_variable(variable, domain): Adds a variable to the CSP with its domain.
    """
    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes a Constraint Satisfaction Problem (CSP) object.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Attributes:
            variables (dict): A dictionary to store the variables of the CSP.
            constraints (list): A list to store the constraints of the CSP.
            unassigned_var (list): A list to store the unassigned variables of the CSP.
            var_constraints (dict): A dictionary to store the constraints associated with each variable.
            assignments (dict): A dictionary to store the assignments of the CSP.
        """
        self.variables = {}
        self.constraints = []
        self.unassigned_var = []
        self.var_constraints = {}
        self.assignments = {}
        self.assignments_number = 0

    def log_state(self, removed_values: List[Tuple[any, any]], step_description: str = "") -> None:
        print(f"\n{'='*30} {step_description} {'='*30}")
        print("Assignments:")
        for variable, value in self.assignments.items():
            print(f"  {variable}: {value if value is not None else 'Unassigned'}")
        
        print("\nDomains:")
        for variable, domain in self.variables.items():
            print(f"  {variable}: {domain}")
        
        print("\nRemoved Values:")
        for variable, value in removed_values:
            print(f"  {variable}: {value}")
    
    print("="*75)


    def add_constraint(self, constraint_func: Callable, variables: List) -> None:
        """
        Adds a constraint to the CSP.

        Args:
            constraint_func (function): The constraint function to be added.
            variables (list): The variables involved in the constraint.

        Returns:
            None
        """
        self.constraints.append((constraint_func, variables))
        for variable in variables:
            if variable not in self.var_constraints:
                self.var_constraints[variable] = []
            self.var_constraints[variable].append(constraint_func)

    def add_variable(self, variable: any, domain: List) -> None:
        """
        Adds a variable to the CSP with its domain.

        Args:
            variable: The variable to be added.
            domain: The domain of the variable.

        Returns:
            None
        """
        self.variables[variable] = domain[:]
        self.unassigned_var.append(variable)
        self.assignments[variable] = None

    def assign(self, variable: any, value: any) -> None:
        """
        Assigns a value to a variable in the CSP.

        Args:
            variable (any): The variable to be assigned.
            value (any): The value to be assigned to the variable.

        Returns:
            nothing
        """
        self.assignments[variable] = value
        self.unassigned_var.remove(variable)
        self.assignments_number += 1

    
    def is_consistent(self, variable: any, value: any) -> bool:
        """
        Checks if assigning a value to a variable violates any constraints.

        Args:
            variable (any): The variable to be assigned.
            value (any): The value to be assigned to the variable.

        Returns:
            bool: True if the assignment is consistent with the constraints, False otherwise.
        """
        temp_assignment = self.assignments.copy()
        temp_assignment[variable] = value
        for constraint_func, vars_in_constraint in self.constraints:
            if variable in vars_in_constraint:
                values = [temp_assignment[var] for var in vars_in_constraint]
                if None not in values and not constraint_func(*values):
                    return False
        return True

    def is_complete(self) -> bool:
        """
        Checks if the CSP is complete, i.e., all variables have been assigned.

        Returns:
            bool: True if the CSP is complete, False otherwise.
        """
        return len(self.unassigned_var) == 0
    

    def is_assigned(self, variable: any) -> bool:
        """
        Checks if a variable has been assigned a value.

        Args:
            variable (str): The variable to check.

        Returns:
            bool: True if the variable has been assigned, False otherwise.
        """
        return self.assignments[variable] is not None

    def un_assign(self, removed_values_from_domain: List[Tuple[any, any]], variable: any) -> None:
        self.log_state(removed_values_from_domain, f"Before Unassigning {variable}")
        
        self.assignments[variable] = None
        if variable not in self.unassigned_var:
            self.unassigned_var.append(variable)

        for var, value in removed_values_from_domain:
            if value not in self.variables[var]:  
                self.variables[var].append(value)

        for var in self.variables:
            self.variables[var].sort()

        self.log_state(removed_values_from_domain, f"After Unassigning {variable}")




