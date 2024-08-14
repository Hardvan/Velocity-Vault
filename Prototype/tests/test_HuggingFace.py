# Run as follows:
# cd to Prototype
# python -m unittest tests.test_HuggingFace


import unittest
from HuggingFace import sentiment_analysis, summarize_text


class TestHuggingFace(unittest.TestCase):

    def test_sentiment_analysis_positive(self):
        text = "I love this product."
        result = sentiment_analysis(text)
        self.assertEqual(result['label'], 'POSITIVE',
                         "The sentiment should be classified as POSITIVE.")
        self.assertGreater(
            result['score'], 0.9, "The confidence score should be greater than 0.9.")

    def test_sentiment_analysis_negative(self):
        text = "I hate this product."
        result = sentiment_analysis(text)
        self.assertEqual(result['label'], 'NEGATIVE',
                         "The sentiment should be classified as NEGATIVE.")
        self.assertGreater(
            result['score'], 0.9, "The confidence score should be greater than 0.9.")

    def test_summarize_text_long_input(self):
        text = """I recently took the plunge into the electric vehicle world, and my choice was the Tesla Cybertruck. 
                  To say I'm impressed would be an understatement - this beast of a machine is a game-changer. 
                  The futuristic design turns heads wherever I go, and the stainless-steel exoskeleton not only looks 
                  badass but also feels indestructible."""
        result = summarize_text(text)
        self.assertLess(len(result['summary_text'].split()), len(
            text.split()), "The summary should be shorter than the input.")


if __name__ == "__main__":
    unittest.main()
