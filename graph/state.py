from typing import TypedDict


class ReviewState(TypedDict):
    article: str

    grammar_score: int
    grammar_feedback: str

    seo_score: int
    seo_feedback: str

    readability_score: int
    readability_feedback: str

    improved_article: str