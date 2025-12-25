variables = ["A", "B", "C"]

domains = {
    "A": ["red", "green", "blue"],
    "B": ["red", "green", "blue"],
    "C": ["red", "green", "blue"]
}

constraints = {
    ("A", "B"),
    ("B", "C"),
    ("A", "C")
}


def neighbors(var):
    return {y if x == var else x
            for (x, y) in constraints if var in (x, y)}


def is_valid(assignment, var, value):
    for n in neighbors(var):
        if n in assignment and assignment[n] == value:
            return False
    return True


# 🧠 MRV + Degree
def select_variable(assignment):
    unassigned = [v for v in variables if v not in assignment]

    # MRV
    min_domain = min(len(domains[v]) for v in unassigned)
    mrv_vars = [v for v in unassigned if len(domains[v]) == min_domain]

    # Degree heuristic
    return max(mrv_vars, key=lambda v: len(neighbors(v)))


# 🧠 LCV
def order_values(var, assignment):
    def conflicts(value):
        return sum(
            1 for n in neighbors(var)
            if n not in assignment and value in domains[n]
        )
    return sorted(domains[var], key=conflicts)


def backtrack(assignment):
    if len(assignment) == len(variables):
        return assignment

    var = select_variable(assignment)

    for value in order_values(var, assignment):
        if is_valid(assignment, var, value):
            assignment[var] = value
            result = backtrack(assignment)
            if result:
                return result
            del assignment[var]

    return None


solution = backtrack({})
print("Розв’язок з евристиками:", solution)
