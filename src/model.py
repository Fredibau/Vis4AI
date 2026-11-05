"""Laya Multilingual: https://huggingface.co/convaiinnovations/laya-multilingual

Not a plain transformers classifier: it is loaded via the `laya` package and answers
"typed questions" about a state. Weights (~640 MB) are cached by huggingface_hub on first load.
If loading hangs, set the env var USE_TF=0 (see model card).
"""
import laya

MODEL_ID = "convaiinnovations/laya-multilingual"


def load_model():
    return laya.load(MODEL_ID)


def intent_question(options: dict[str, str]) -> dict:
    """options: {intent_label: short description}.
    NOTE: model card says keep choice questions < ~20 options; MASSIVE has 60 intents
    -> group must decide (e.g. ask per scenario, or a fixed 20-intent subset like the card's benchmark)."""
    return {"intent": {"type": "choice",
                       "instructions": "What does the user want the assistant to do in `body`?",
                       "criteria": options}}


if __name__ == "__main__":  # smoke test
    agent = load_model()
    q = intent_question({"alarm_set": "set an alarm", "weather_query": "ask about the weather",
                         "play_music": "play a song or music"})
    for text in ["wake me up at seven", "wird es morgen regnen", "mets ma chanson préférée"]:
        print(text, "->", agent.predict({"body": text}, q)["answers"]["intent"])
