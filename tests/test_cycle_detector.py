import unittest

def has_cyclic_loops(mls_units):
    adj_matrix = {unit['mls_id']: unit['dependencies'] for unit in mls_units}
    visited = {}
    
    def dfs(node):
        if node in visited:
            return visited[node]
        visited[node] = True
        for dep in adj_matrix.get(node, []):
            if dep in adj_matrix and dfs(dep):
                return True
        visited[node] = False
        return False

    for unit in mls_units:
        if dfs(unit['mls_id']):
            return True
    return False

class TestMlsDagCycles(unittest.TestCase):
    def test_valid_dag_passes(self):
        valid_payload = [
            {"mls_id": "MLS-01", "dependencies": []},
            {"mls_id": "MLS-02", "dependencies": ["MLS-01"]}
        ]
        self.assertFalse(has_cyclic_loops(valid_payload))

    def test_cyclic_dag_fails(self):
        invalid_payload = [
            {"mls_id": "MLS-01", "dependencies": ["MLS-02"]},
            {"mls_id": "MLS-02", "dependencies": ["MLS-01"]}
        ]
        self.assertTrue(has_cyclic_loops(invalid_payload))

if __name__ == '__main__':
    unittest.main()
