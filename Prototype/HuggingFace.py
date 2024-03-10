from transformers import pipeline


def sentiment_analysis(text):
    """Run sentiment analysis on the input text.

    Args
    ----
    - text (str): The input text to analyze.

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
    - text (str): The input text to summarize.

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
            """New York (CNN)When Liana Barrientos was 23 years old, she got married in Westchester County, New York.
A year later, she got married again in Westchester County, but to a different man and without divorcing her first husband.
Only 18 days after that marriage, she got hitched yet again. Then, Barrientos declared "I do" five more times, sometimes only within two weeks of each other.
In 2010, she married once more, this time in the Bronx. In an application for a marriage license, she stated it was her "first and only" marriage.
Barrientos, now 39, is facing two criminal counts of "offering a false instrument for filing in the first degree," referring to her false statements on the
2010 marriage license application, according to court documents.
Prosecutors said the marriages were part of an immigration scam.
On Friday, she pleaded not guilty at State Supreme Court in the Bronx, according to her attorney, Christopher Wright, who declined to comment further.
After leaving court, Barrientos was arrested and charged with theft of service and criminal trespass for allegedly sneaking into the New York subway through an emergency exit, said Detective
Annette Markowski, a police spokeswoman. In total, Barrientos has been married 10 times, with nine of her marriages occurring between 1999 and 2002.
All occurred either in Westchester County, Long Island, New Jersey or the Bronx. She is believed to still be married to four men, and at one time, she was married to eight men at once, prosecutors say.
Prosecutors said the immigration scam involved some of her husbands, who filed for permanent residence status shortly after the marriages.
Any divorces happened only after such filings were approved. It was unclear whether any of the men will be prosecuted.
The case was referred to the Bronx District Attorney\'s Office by Immigration and Customs Enforcement and the Department of Homeland Security\'s
Investigation Division. Seven of the men are from so-called "red-flagged" countries, including Egypt, Turkey, Georgia, Pakistan and Mali.
Her eighth husband, Rashid Rajput, was deported in 2006 to his native Pakistan after an investigation by the Joint Terrorism Task Force.
If convicted, Barrientos faces up to four years in prison.  Her next court appearance is scheduled for May 18.
    """
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
