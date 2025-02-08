from collections import deque
from typing import Callable, List, Tuple, Any
from CSP import CSP


class Solver(object):

    def __init__(self, csp: CSP, domain_heuristics: bool = False, variable_heuristics: bool = False, MAC: bool = False) -> None:
        """
        Initializes a Solver object.

        Args:
            csp (CSP): The Constraint Satisfaction Problem to be solved.
            domain_heuristics (bool, optional): Flag indicating whether to use domain heuristics. Defaults to False.
            variable_heuristics (bool, optional): Flag indicating whether to use variable heuristics. Defaults to False.
            AC_3 (bool, optional): Flag indicating whether to use the AC-3 algorithm. Defaults to False.
            MAC (bool, optional): Flag indicating whether to use the MAC algorithm. Defaults to False.
        """
        self.domain_heuristic = domain_heuristics
        self.variable_heuristic = variable_heuristics
        self.MAC = MAC
        self.csp = csp
        self.board_size = int(len(self.csp.variables) ** 0.5)


    def backtrack_solver(self) -> None | dict:
        """
        Backtracking algorithm to solve the constraint satisfaction problem (CSP).

        Returns:
            dict{any : any}: A list of variable-value assignments that satisfy all constraints.
        """
        if self.csp.is_complete():
            # Convert string keys like "1,2" to tuples (1, 2)
            return {tuple(map(int, key.split(","))): value for key, value in self.csp.assignments.items()}

        variable = self.select_unassigned_variable()
        domain = self.ordered_domain_value(variable)

        for value in domain:
            if self.csp.is_consistent(variable, value):
                self.csp.assign(variable, value)
                removed_values = self.apply_MAC() if self.MAC else []
                print(f"Removed Values: {removed_values}")
                print(f"Current Variable: {variable}")
                result = self.backtrack_solver()
                if result:
                    return result


                self.csp.un_assign(removed_values, variable)

        return None


    def select_unassigned_variable(self) -> any:
        """
        Selects an unassigned variable using the MRV heuristic or Random.

        Returns:
            any: The selected unassigned variable.
        """
        if self.variable_heuristic:
            return self.MRV(self.csp.unassigned_var)
        return self.csp.unassigned_var[0]
    

    def ordered_domain_value(self, variable: str) -> List[Any]:
        """
        Returns a list of domain values for the given variable in a specific order.

        Args:
            variable (any): The name of the variable.

        Returns:
            List[any]: A list of domain values for the variable in a specific order.
        """
        if self.domain_heuristic:
            return self.LCV(variable)
        return self.csp.variables[variable]

    def apply_MAC(self) -> List[Tuple[Any, Any]]:
        queue = deque()
        removed_values = []

        for constraint_func, variables in self.csp.constraints:
            for i in range(len(variables)):
                for j in range(len(variables)):
                    if i != j:
                        queue.append((variables[i], variables[j], constraint_func))

        self.csp.log_state(removed_values, "Initial State Before MAC")

        while queue:
            x, y, constraint_func = queue.popleft()
            removed = self.binary_arc_reduce(x, y, constraint_func)

            if removed:
                removed_values.extend((x, value) for value in removed)

                self.csp.log_state(removed_values, f"After Reducing {x} -> {y}")

                if not self.csp.variables[x]: 
                    return removed_values
                for related_constraint in self.csp.var_constraints.get(x, []):
                    for z in self.csp.variables:
                        if z != x and z in self.csp.var_constraints:
                            queue.append((z, x, related_constraint))

        self.csp.log_state(removed_values, "Final State After MAC")
        return removed_values
    

    def binary_arc_reduce(self, x: Any, y: Any, constraint_func: Callable) -> List[Any]:
        removed = []
        for value_x in self.csp.variables[x][:]:
            is_consistent = any(constraint_func(value_x, value_y) for value_y in self.csp.variables[y])
            if not is_consistent:
                print(f"value deleted : {value_x}")
                print(f"value  : {self.csp.variables[x]}")
                removed.append(value_x)
                self.csp.variables[x].remove(value_x)
        return removed





    def multi_arc_reduce(self, constraint_func: Callable, variables: List[Any]) -> List[Tuple[Any, Any]]:
        """
        Reduces the domains of variables based on the specified constraint.

        This function examines the current assignments of the given variables
        and removes values from their domains that are inconsistent with the
        provided constraints.

        Args:
            constraint_func (Callable): The constraint function defining the relationship between variables.
            variables (List[Any]): A list of variable names whose domains are to be reduced.

        Returns:
            List[Tuple[Any, Any]]: A list of removed values from domains.
        """
        removed_values = []
        for var in variables:
            temp_assignment = self.csp.assignments.copy()
            for value in self.csp.variables[var]:
                temp_assignment[var] = value
                values = [temp_assignment.get(v, None) for v in variables]
                if None not in values and not constraint_func(*values):
                    removed_values.append((var, value))
            for var, value in removed_values:
                if value in self.csp.variables[var]:
                    self.csp.variables[var].remove(value)
        return removed_values



    def MRV(self, variables) -> Any:
        """
        Selects the variable with the Minimum Remaining Values (MRV) heuristic.

        Returns:
            Any: The variable with the fewest remaining values.
        """
        return min(variables, key=lambda var: len(self.csp.variables[var]))

    def LCV(self, variable: Any) -> List[Any]:
        """
        Orders the values of a variable based on the Least Constraining Value (LCV) heuristic.

        Args:
            variable (Any): The variable for which to order the values.

        Returns:
            List[Any]: A list of values sorted based on the number of constraints they impose.
        """
        def count_constraints(value):
            count = 0
            temp_assignment = self.csp.assignments.copy()
            temp_assignment[variable] = value
            for constraint_func, vars_in_constraint in self.csp.constraints:
                if variable in vars_in_constraint:
                    if not constraint_func(*[temp_assignment.get(v, None) for v in vars_in_constraint]):
                        count += 1
            return count

        return sorted(self.csp.variables[variable], key=count_constraints)
