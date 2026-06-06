from langgraph.graph import StateGraph

from graph.state import ReviewState
from graph.nodes import (
    grammar_review,
    seo_review,
    readability_review,
    rewrite_article,
)

builder = StateGraph(ReviewState)

builder.add_node("grammar_review", grammar_review)
builder.add_node("seo_review", seo_review)
builder.add_node("readability_review", readability_review)
builder.add_node("rewrite_article", rewrite_article)

builder.set_entry_point("grammar_review")

builder.add_edge("grammar_review", "seo_review")
builder.add_edge("seo_review", "readability_review")
builder.add_edge("readability_review", "rewrite_article")

builder.set_finish_point("rewrite_article")

graph = builder.compile()