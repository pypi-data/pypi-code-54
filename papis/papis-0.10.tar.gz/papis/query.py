import typing as t


class Term:
    def __init__(self) -> None:
        self.terms = []  # type: t.Sequence[Term]

    def __iter__(self) -> t.Iterator["Term"]:
        return iter(self.terms)

    def __getitem__(self, key: int) -> "Term":
        return self.terms[key]


class Simple(Term):
    def __init__(self) -> None:
        self.terms = []


class Or(Term):
    def __init__(self, terms: t.Sequence[Term]):
        self.terms = []
        for tm in terms:
            if isinstance(tm, self.__class__):
                self.terms.extend(tm.terms)
            else:
                self.terms.append(tm)


class And(Term):
    def __init__(self, terms: t.Sequence[Term]):
        # self.terms will be a list of Or's or Simple terms
        self.terms = []
        for tm in terms:
            if isinstance(tm, self.__class__):
                self.terms.extend(tm.terms)
            else:
                self.terms.append(tm)


def expand(expr: Term) -> Term:
    if isinstance(expr, Simple):
        return expr
    elif isinstance(expr, Or):
        return Or([expand(tm) for tm in expr])
    elif isinstance(expr, And):
        if isinstance(expr[0], Or):
            return And([expand(e) for e in expr])
        else:
            return
            # return Or([expr[0]] +
        return And([expand(e) for e in expr])
    else:
        raise ValueError("Invalid expr")
