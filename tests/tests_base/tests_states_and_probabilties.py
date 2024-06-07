import unittest
from base.results import StatesAndProbabilities

class TestStatesAndProbabilities(unittest.TestCase):

    def setUp(self):
        self.sap = StatesAndProbabilities()
        self.sap.set_probability('|1,0>', 0.5)
        self.sap.set_counting('|1,0>', 10)

    def test_set_and_get_probability(self):
        self.sap.set_probability('|0,1>', 0.3)
        self.assertEqual(self.sap.get_probability('|0,1>'), 0.3)
        self.assertIsNone(self.sap.get_probability('|0,0>'))

    def test_set_and_get_counting(self):
        self.sap.set_counting('|0,1>', 5)
        self.assertEqual(self.sap.get_counting('|0,1>'), 5)
        self.assertIsNone(self.sap.get_counting('|0,0>'))

    def test_has_countings(self):
        self.assertTrue(self.sap.has_countings())
        self.sap.set_counting('|1,0>', 0)
        self.assertTrue(self.sap.has_countings())

    def test_has_probabilities(self):
        self.assertTrue(self.sap.has_probabilities())
        self.sap.set_probability('|1,0>', 0)
        self.assertTrue(self.sap.has_probabilities())

    def test_aggregate(self):
        results_to_aggregate = {'|0,1>': 0.3, '|1,1>': 0.2}
        self.sap.aggregate(results_to_aggregate, operation='+')
        expected = {
            '|1,1>': 0.8,  # 0.5 (|1,0>) + 0.3 (|0,1>)
            '|2,1>': 0.7,  # 0.5 (|1,0>) + 0.2 (|1,1>)
        }
        self.assertEqual(self.sap.states_and_probabilities, expected)

if __name__ == "__main__":
    unittest.main()
