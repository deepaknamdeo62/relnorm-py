
# relnorm-py

**relnorm-py** is an open-source Python library and utility for analyzing Relational Database Schemas, computing Attribute Closures ($X^+$), discovering Candidate Keys, and diagnosing Normal Form violations (2NF, 3NF, and BCNF).

## Features
- **Attribute Closure Computation:** Fast fixed-point evaluation of $X^+$ under a given set of Functional Dependencies (FDs).
- **Candidate Key Discovery:** Automatically identifies all minimal superkeys and prime attributes.
- **Normal Form Diagnostics:** Evaluates schemas against 2NF, 3NF, and BCNF rules with detailed violation explanations (partial and transitive dependencies).

## Quick Start

```python
from relnorm import RelationSchema

attrs = {"A", "B", "C", "D"}
fds = [({"A"}, {"B"}), ({"B"}, {"C"}), ({"A"}, {"D"})]

schema = RelationSchema(attrs, fds)
report = schema.analyze_normal_forms()

print("Candidate Keys:", report["candidate_keys"])
print("Highest Normal Form:", report["highest_normal_form"])
