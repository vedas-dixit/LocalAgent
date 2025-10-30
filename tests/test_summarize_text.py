from tools.summarize_text import summarize_text


def test_summarize_text_returns_string():
    text = (
        "Large Language Models (LLMs) are increasingly used for summarization. "
        "We need a brief, structured summary with a key takeaway."
    )
    res = summarize_text.run(text)
    assert isinstance(res, str)
    assert len(res) > 0
