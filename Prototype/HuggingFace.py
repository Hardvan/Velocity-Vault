from transformers import pipeline
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


def sentiment_analysis(text):
    """Run sentiment analysis on the input text.

    Args
    ----
    - `text`: The input text to analyze.

    Returns
    -------
    - list: A list of dictionaries containing the label and score of the sentiment analysis.
        - Structure: {'label': '...', 'score': ...}
    """

    classifier = pipeline('sentiment-analysis')
    result = classifier(text)
    return result[0]  # {'label': '...', 'score': ...}


def summarize_text(text):
    """Run summarization on the input text.

    Args
    ----
    - `text`: The input text to summarize.

    Returns
    -------
    - list: A list of dictionaries containing the summary of the input text.
        - Structure: {'summary_text': '...'}
    """

    summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
    result = summarizer(text, min_length=10, max_length=100, do_sample=False)
    return result[0]  # {'summary_text': '...'}


if __name__ == "__main__":

    import time

    def test_sentiment_analysis():

        print("Testing sentiment analysis...")

        start = time.time()

        # Sample input texts
        input_texts = [
            "I love this product.",
            "I hate this product.",
            "I am not sure about this product.",
            "I am feeling happy.",
            "I am feeling sad.",
            "I am feeling neutral.",
            "The product has a good quality, but is too expensive.",
            "The product is cheap, but has a bad quality.",
            "The product is neither good nor bad."
        ]

        # Run sentiment analysis on the input texts
        output = []
        for text in input_texts:
            result = sentiment_analysis(text)
            output.append({
                "input_text": text,
                "label": result['label'],
                "score": result['score']
            })

        # Save the results to a markdown file
        file_name = "test/sentiment_analysis.md"
        file_heading = "# Test Sentiment Analysis\n\n"
        table_header = "| Input text | Label | Score |\n"
        table_divider = "| --- | --- | --- |\n"
        table_rows = ""
        for result in output:
            row = f"| {result['input_text']} | {result['label']} | {result['score']} |\n"
            table_rows += row
        markdown_table = file_heading + table_header + table_divider + table_rows
        with open(file_name, "w") as file:
            file.write(markdown_table)

        end = time.time()
        print(
            f"✅ Test Sentiment Analysis completed in {end - start:.2f} seconds.")

    def test_summarize_text():

        print("Testing summarize text...")

        start = time.time()

        # Input news stories
        news_stories = [
            """I recently took the plunge into the electric vehicle world, and my choice was the Tesla Cybertruck. To say I'm impressed would be an understatement - this beast of a machine is a game-changer. The futuristic design turns heads wherever I go, and the stainless-steel exoskeleton not only looks badass but also feels indestructible. 

Driving the Cybertruck is an experience like no other. The acceleration is mind-blowing, and the electric motor's silent hum adds an unexpected touch of serenity. The interior is a minimalist masterpiece, with a massive touchscreen that seamlessly controls everything from climate to entertainment. The autopilot feature is a game-changer on long drives, making the journey not just efficient but downright enjoyable.

Charging is a breeze with Tesla's Supercharger network, and the range is more than sufficient for my daily commute and spontaneous road trips. The Cybertruck has exceeded my expectations, and I now find excuses to drive just for the sheer pleasure of it. Tesla has truly set the bar high with this innovative and futuristic vehicle. Highly recommend for anyone ready to embrace the future of transportation!"""
        ]

        # Run summarization on the news stories
        output = []
        for story in news_stories:
            result = summarize_text(story)
            output.append({
                "input_text": story,
                "summary_text": result['summary_text']
            })

        # Save the results to a markdown file
        file_name = "test/summarize_text.md"
        with open(file_name, "w") as file:
            for result in output:
                file.write("# Test Summarize Text\n\n")
                input_text = result['input_text']
                input_size = len(input_text.split(" "))
                summary_text = result['summary_text']
                summary_size = len(summary_text.split(" "))
                file.write("## Input Text\n\n")
                file.write(f"{input_text}\n\n")
                file.write("## Input Size\n\n")
                file.write(f"{input_size} words\n\n")
                file.write("## Summary\n\n")
                file.write(f"{summary_text}\n\n")
                file.write("## Summary Size\n\n")
                file.write(f"{summary_size} words\n\n")

        end = time.time()
        print(f"✅ Test Summarize Text completed in {end - start:.2f} seconds.")

    test_sentiment_analysis()
    test_summarize_text()
