import unittest

from lsb import dag


def units(*pairs):
    return [{"mls_id": uid, "dependencies": list(deps)} for uid, deps in pairs]


class FindCycle(unittest.TestCase):
    # The two cases from the original tests/test_cycle_detector.py.
    def test_valid_dag_passes(self):
        self.assertIsNone(dag.find_cycle(units(("MLS-01", []), ("MLS-02", ["MLS-01"]))))

    def test_two_node_cycle_fails(self):
        cycle = dag.find_cycle(units(("MLS-01", ["MLS-02"]), ("MLS-02", ["MLS-01"])))
        self.assertEqual(cycle[0], cycle[-1])
        self.assertEqual(set(cycle), {"MLS-01", "MLS-02"})

    def test_self_dependency_is_a_cycle(self):
        self.assertEqual(dag.find_cycle(units(("A", ["A"]))), ["A", "A"])

    def test_cycle_downstream_of_acyclic_root(self):
        cycle = dag.find_cycle(units(("A", ["B"]), ("B", ["C"]), ("C", ["D"]), ("D", ["B"])))
        self.assertEqual(cycle, ["B", "C", "D", "B"])

    def test_diamond_is_not_a_cycle(self):
        self.assertFalse(dag.has_cycle(units(("A", []), ("B", ["A"]), ("C", ["A"]), ("D", ["B", "C"]))))

    def test_missing_dependency_is_not_a_cycle(self):
        self.assertFalse(dag.has_cycle(units(("A", ["GHOST"]))))

    def test_long_chain_does_not_hit_recursion_limit(self):
        chain = [("N0", [])] + [(f"N{i}", [f"N{i-1}"]) for i in range(1, 5000)]
        self.assertFalse(dag.has_cycle(units(*chain)))


class OtherGraphChecks(unittest.TestCase):
    def test_missing_dependencies(self):
        self.assertEqual(dag.missing_dependencies(units(("A", []), ("B", ["A", "Z"]))), [("B", "Z")])

    def test_duplicate_ids(self):
        self.assertEqual(dag.duplicate_ids(units(("A", []), ("A", []), ("B", []))), ["A"])

    def test_topological_order(self):
        order = dag.topological_order(units(("D", ["B", "C"]), ("B", ["A"]), ("C", ["A"]), ("A", [])))
        self.assertEqual(order, ["A", "B", "C", "D"])

    def test_topological_order_rejects_cycle(self):
        with self.assertRaises(ValueError):
            dag.topological_order(units(("A", ["B"]), ("B", ["A"])))


if __name__ == "__main__":
    unittest.main()
