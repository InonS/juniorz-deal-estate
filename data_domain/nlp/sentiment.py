"""
Sentiment analysis using Hugging Face Transformers (PyTorch backend).
"""
from typing import List
from transformers import pipeline
from ..utils import config

def analyze_sentiment(texts: List[str], model_name: str = config.HF_SENTIMENT_MODEL) -> List[str]:
    """
    Sentiment analysis using a Hugging Face Transformers pipeline.

    Args:
        texts: List of texts to analyze.
        model_name: Name of the HuggingFace model to use.

    Returns:
        List of sentiment labels ('POSITIVE', 'NEGATIVE', etc.).

    >>> analyze_sentiment(["This is great!", "Awful experience."])  # doctest: +SKIP
    ['POSITIVE', 'NEGATIVE']
    """
    classifier = pipeline("sentiment-analysis", model=model_name)
    results = classifier(texts)
    return [res['label'] for res in results]

def main() -> None:
    """
    CLI entrypoint for sentiment analysis.

    Usage: python -m data_domain.nlp.sentiment "Text 1" "Text 2"

    >>> # Should be run from CLI, not as doctest.
    """
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m data_domain.nlp.sentiment \"Text 1\" \"Text 2\" ...")
        return
    texts = sys.argv[1:]
    sentiments = analyze_sentiment(texts)
    for text, sentiment in zip(texts, sentiments):
        print(f"Text: {text!r} -> Sentiment: {sentiment}")

if __name__ == "__main__":
    main()