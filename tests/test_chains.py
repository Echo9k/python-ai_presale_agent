import unittest
from chains.proposal_chain import build_cost_chain

class TestChains(unittest.TestCase):
    def test_cost_chain(self):
        chain = build_cost_chain()
        sample_input = {"project_details": "Test project"}
        result = chain.run(sample_input)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

if __name__ == '__main__':
    unittest.main()
