# tests for the signal tracker
# these use fake versions of hacker news and gemini so they don't need internet or an api key

import os
import sys
import pandas as pd

# so python can find the files in the main folder
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import fetch_data
import analyze_trends
import save_trends


# fake stuff

class FakeHNResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {"hits": [
            {"title": "Acme lays off 10%", "url": "https://a.com", "points": 50},
            {"title": None, "url": "https://b.com", "points": 5},
            {"title": "Beta is hiring", "url": "https://c.com", "points": 20},
        ]}


class FakeReply:
    def __init__(self, text):
        self.text = text


class FakeModels:
    def __init__(self, text):
        self.text = text

    def generate_content(self, model, contents):
        return FakeReply(self.text)


class FakeGemini:
    def __init__(self, text):
        self.models = FakeModels(text)


fake_json = '{"signals": [{"company": "Acme", "signal_type": "layoff", "description": "Acme cut 10% of staff."}]}'


# the actual tests

def test_fetch_skips_stories_with_no_title(monkeypatch):
    monkeypatch.setattr(fetch_data.requests, "get", lambda *args, **kwargs: FakeHNResponse())
    stories = fetch_data.fetch_hn_stories("anything")
    assert len(stories) == 2


def test_gemini_plain_json():
    result = analyze_trends.ask_gemini_for_signals([{"title": "x"}], client=FakeGemini(fake_json))
    assert result["signals"][0]["company"] == "Acme"


def test_gemini_json_with_backticks():
    reply = "```json\n" + fake_json + "\n```"
    result = analyze_trends.ask_gemini_for_signals([{"title": "x"}], client=FakeGemini(reply))
    assert result["signals"][0]["signal_type"] == "layoff"


def test_save_adds_to_csv(tmp_path, monkeypatch):
    # use a temporary csv so the real one doesn't get messed up
    test_file = str(tmp_path / "test_log.csv")
    monkeypatch.setattr(save_trends, "LOG_FILE", test_file)
    monkeypatch.setattr(save_trends, "fetch_hn_stories", lambda *args, **kwargs: [{"title": "x"}])
    monkeypatch.setattr(save_trends, "ask_gemini_for_signals",
                        lambda headlines: {"signals": [{"company": "Acme", "signal_type": "layoff", "description": "test"}]})

    save_trends.save_signals()
    save_trends.save_signals()

    # running it twice should give 2 rows, not overwrite
    saved = pd.read_csv(test_file)
    assert len(saved) == 2


def test_save_does_nothing_when_no_news(tmp_path, monkeypatch):
    test_file = tmp_path / "test_log.csv"
    monkeypatch.setattr(save_trends, "LOG_FILE", str(test_file))
    monkeypatch.setattr(save_trends, "fetch_hn_stories", lambda *args, **kwargs: [])

    result = save_trends.save_signals()

    # no news means no csv gets made
    assert result is None
    assert not test_file.exists()
