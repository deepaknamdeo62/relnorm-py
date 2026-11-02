"""
relnorm-py: Relational Schema Normalization & Functional Dependency Analyzer
"""
from itertools import combinations
from typing import Set, List, Tuple, Dict


class RelationSchema:
    def __init__(self, attributes: Set[str], fds: List[Tuple[Set[str], Set[str]]]):
        self.attributes = set(attributes)
        self.fds = self._split_rhs(fds)

    @staticmethod
    def _split_rhs(fds: List[Tuple[Set[str], Set[str]]]) -> List[Tuple[Set[str], Set[str]]]:
        canonical = []
        for lhs, rhs in fds:
            for attr in rhs:
                canonical.append((set(lhs), {attr}))
        return canonical

    def closure(self, attrs: Set[str]) -> Set[str]:
        result = set(attrs)
        changed = True
        while changed:
            changed = False
            for lhs, rhs in self.fds:
                if lhs.issubset(result) and not rhs.issubset(result):
                    result.update(rhs)
                    changed = True
        return result

    def is_superkey(self, attrs: Set[str]) -> bool:
        return self.closure(attrs) == self.attributes

    def find_candidate_keys(self) -> List[Set[str]]:
        candidate_keys = []
        n = len(self.attributes)
        sorted_attrs = sorted(self.attributes)

        for r in range(1, n + 1):
            for comb in combinations(sorted_attrs, r):
                comb_set = set(comb)
                if any(ck.issubset(comb_set) for ck in candidate_keys):
                    continue
                if self.is_superkey(comb_set):
                    candidate_keys.append(comb_set)
        return candidate_keys

    def analyze_normal_forms(self) -> Dict[str, object]:
        cks = self.find_candidate_keys()
        prime_attrs = set().union(*cks) if cks else set()

        is_2nf = True
        is_3nf = True
        is_bcnf = True
        violations = []

        for lhs, rhs in self.fds:
            if rhs.issubset(lhs):
                continue

            lhs_is_superkey = self.is_superkey(lhs)
            rhs_is_prime = rhs.issubset(prime_attrs)

            if not lhs_is_superkey:
                is_bcnf = False
                if not rhs_is_prime:
                    is_3nf = False
                    if any(lhs.issubset(ck) and lhs != ck for ck in cks):
                        is_2nf = False
                        violations.append(f"2NF Violation: {lhs} -> {rhs} (Partial Dependency)")
                    else:
                        violations.append(f"3NF Violation: {lhs} -> {rhs} (Transitive Dependency)")
                else:
                    violations.append(f"BCNF Violation: {lhs} -> {rhs} (LHS is not a superkey)")

        highest_nf = "BCNF" if is_bcnf else ("3NF" if is_3nf else ("2NF" if is_2nf else "1NF"))
        return {
            "candidate_keys": cks,
            "prime_attributes": prime_attrs,
            "highest_normal_form": highest_nf,
            "2NF": is_2nf,
            "3NF": is_3nf,
            "BCNF": is_bcnf,
            "violations": violations,
        }


if __name__ == "__main__":
    attrs = {"A", "B", "C", "D"}
    fds = [({"A"}, {"B"}), ({"B"}, {"C"}), ({"A"}, {"D"})]

    schema = RelationSchema(attrs, fds)
    report = schema.analyze_normal_forms()

    print("=== Relational Schema Analysis ===")
    print(f"Attributes         : {sorted(attrs)}")
    print(f"Candidate Keys     : {[sorted(ck) for ck in report['candidate_keys']]}")
    print(f"Prime Attributes   : {sorted(report['prime_attributes'])}")
    print(f"Highest Normal Form: {report['highest_normal_form']}")
    for v in report["violations"]:
        print(f" - {v}")
