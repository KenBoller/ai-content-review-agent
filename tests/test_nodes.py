
import pytest
from unittest.mock import Mock

from graph import nodes


@pytest.mark.parametrize(
    "response,label,expected",
    [
        ("Grammar Score: 7/10", "Grammar", 7),
        ("SEO Score: 8 / 10", "SEO", 8),
        ("Readability Score: 6 out of 10", "Readability", 6),
        ("Grammar Score: 15/10", "Grammar", 10),
        ("Grammar Score: 0/10", "Grammar", 0),
        ("No score provided", "Grammar", 0),
    ],
)
def test_extract_score(response, label, expected):
    assert nodes.extract_score(response, label) == expected


def test_grammar_review(monkeypatch):
    fake_llm = Mock()
    fake_llm.invoke.return_value.content = (
        "Grammar Score: 8/10\nFeedback: Clear writing."
    )
    monkeypatch.setattr(nodes, "llm", fake_llm)

    result = nodes.grammar_review({"article": "Sample article."})

    assert result["grammar_score"] == 8
    assert "Clear writing" in result["grammar_feedback"]
    fake_llm.invoke.assert_called_once()


def test_seo_review(monkeypatch):
    fake_llm = Mock()
    fake_llm.invoke.return_value.content = (
        "SEO Score: 9/10\nFeedback: Good keywords."
    )
    monkeypatch.setattr(nodes, "llm", fake_llm)

    result = nodes.seo_review({"article": "Sample article."})

    assert result["seo_score"] == 9
    fake_llm.invoke.assert_called_once()


def test_readability_review(monkeypatch):
    fake_llm = Mock()
    fake_llm.invoke.return_value.content = (
        "Readability Score: 7/10\nFeedback: Shorten sentences."
    )
    monkeypatch.setattr(nodes, "llm", fake_llm)

    result = nodes.readability_review({"article": "Sample article."})

    assert result["readability_score"] == 7
    fake_llm.invoke.assert_called_once()


def test_rewrite_article(monkeypatch):
    fake_llm = Mock()
    fake_llm.invoke.return_value.content = "Improved article."
    monkeypatch.setattr(nodes, "llm", fake_llm)

    result = nodes.rewrite_article({
        "article": "Original article.",
        "style_guide": "Use a friendly tone.",
    })

    assert result["improved_article"] == "Improved article."
    assert "Use a friendly tone." in fake_llm.invoke.call_args.args[0]


def test_meta_description_generator(monkeypatch):
    fake_llm = Mock()
    fake_llm.invoke.return_value.content = "  A useful description.  "
    monkeypatch.setattr(nodes, "llm", fake_llm)

    result = nodes.meta_description_generator({
        "article": "Sample article."
    })

    assert result["meta_description"] == "A useful description."


def test_seo_title_generator(monkeypatch):
    fake_llm = Mock()
    fake_llm.invoke.return_value.content = (
        "  1. First Title\n2. Second Title\n3. Third Title  "
    )
    monkeypatch.setattr(nodes, "llm", fake_llm)

    result = nodes.seo_title_generator({
        "article": "Sample article."
    })

    assert result["seo_titles"].startswith("1. First Title")
