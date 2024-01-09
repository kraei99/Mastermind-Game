import unittest
from mastermind_game import compare_guess  # Import the specific function from your game code

class TestMastermindGame(unittest.TestCase):
    def test_guess_comparison(self):
        # Test 1: All colors and placements correct
        secret_code = ["red", "green", "blue", "yellow"]
        user_guess = ["red", "green", "blue", "yellow"]
        result = compare_guess(secret_code, user_guess)
        self.assertEqual(result, (4, 0))  # Expecting 4 correct placements, 0 incorrect

    def test_correct_colors_wrong_placement(self):
        # Test 2: Some correct colors but wrong placements
        secret_code = ["red", "green", "blue", "yellow"]
        user_guess = ["yellow", "red", "green", "blue"]
        result = compare_guess(secret_code, user_guess)
        self.assertEqual(result, (0, 4))  # Expecting 0 correct placements, 4 incorrect

if __name__ == '__main__':
    unittest.main()
