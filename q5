# Question 5 — Movie Review Extraction
# LLM-backed JSON pipeline using qwen3-0.6b

import json

from openai import OpenAI

# ---------------------------------------------------------------------------
# connection
# ---------------------------------------------------------------------------
llm = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
)
MODEL_NAME = "qwen3-0.6b"


# ---------------------------------------------------------------------------
# tiny wrappers
# ---------------------------------------------------------------------------
def ask_llm(prompt: str, system: str) -> str:
    """fire the request, hand back the raw text"""
    resp = llm.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        temperature=0.0,
    )
    return resp.choices[0].message.content


def build_prompt(review: str) -> str:
    """build the extraction prompt, single JSON object only"""
    return (
        "You parse movie reviews. Given the text below, emit ONE JSON document only.\n"
        'Schema: {"title": "<string>", "rating": <int 1..10>, "sentiment": "<positive|negative>"}\n'
        "No markdown. No explanations. No code fences. The movie name goes in 'title', "
        "the score is a whole number from 1 to 10, and sentiment reflects whether the "
        "review was favourable (positive) or not (negative).\n\n"
        f"Review text:\n{review}"
    )


# ---------------------------------------------------------------------------
# parse + validate
# ---------------------------------------------------------------------------
def parse(s: str):
    try:
        return json.loads(s)
    except (json.JSONDecodeError, TypeError):
        return None


def check_review(obj) -> str:
    """returns '' when ok, else a description of what's wrong"""
    if not isinstance(obj, dict):
        return "not a json object"

    want = {"title", "rating", "sentiment"}
    if set(obj.keys()) != want:
        return f"expected keys {sorted(want)} but got {sorted(obj.keys())}"

    title = obj.get("title")
    if isinstance(title, str) is False or title.strip() == "":
        return "title empty"

    rating = obj.get("rating")
    if isinstance(rating, bool) or isinstance(rating, int) is False:
        return "rating is not an int"
    if rating < 1 or rating > 10:
        return f"rating out of range: {rating}"

    sentiment = obj.get("sentiment")
    if sentiment not in ("positive", "negative"):
        return f"bad sentiment: {sentiment!r}"

    return ""


# ---------------------------------------------------------------------------
# retry loop
# ---------------------------------------------------------------------------
def extract_with_retry(review: str, attempts: int = 3) -> dict:
    """try a few times, feeding back the validation error on retries"""
    sys = "You always respond with valid JSON only."
    why = ""
    for i in range(1, attempts + 1):
        if i == 1:
            p = build_prompt(review)
        else:
            p = build_prompt(review) + (
                "\n\nPrevious attempt was rejected: " + why +
                "\nRe-send only corrected JSON using the exact schema."
            )

        raw = ask_llm(p, sys)
        obj = parse(raw)
        why = check_review(obj)
        if why == "":
            return obj

    print(f"[!] Gave up on: {review!r} -- {why}")
    return None


# ---------------------------------------------------------------------------
# reviews (fresh ones this time)
# ---------------------------------------------------------------------------
TEXTS = [
    "saw Oppenheimer with my flatmates, honestly didn't think three hours could fly by "
    "that fast. gorgeous visuals, loud and intense, i'd say a solid 9, loved it.",

    "Gladiator II? big sword, big shield, big everything. story was a bit thin though, "
    "felt like a 6 maybe a 7? visually nice, didn't hate it, didn't love it. whatever, "
    "give it a 7, it was fine",

    "Barbie honestly surprised me, way smarter than i expected, funny and pink and "
    "kind of deep?? i'm going 8, definitely positive",

    "Killers of the Flower Moon is LONG. three and a half hours and my back hurt. "
    "brilliant acting but so slow, some will love it some will hate it, i sit at a 5, "
    "mixed feelings, call it negative i guess",

    "The Marvels was a mess, plain and simple, jokes fell flat, plot was all over, "
    "i walked out bored, that's a 3, negative all the way",

    "Aftersun destroyed me, so quiet and sad and beautiful, i cried at the end, "
    "10/10, one of the best things i've seen recently, absolutely positive",

    "Poor Things is weird, no other way to say it, bizarre and funny and gorgeous, "
    "i think i liked it? it's a 7, i'll say positive, maybe?"
]


# ---------------------------------------------------------------------------
# output
# ---------------------------------------------------------------------------
def process(data, temp=0.0):
    """run everything through the extractor and print a table"""
    orig = llm.chat.completions.create
    llm.chat.completions.create = lambda *a, **kw: orig(*a, **{**kw, "temperature": temp})

    rows = []
    for t in data:
        entry = extract_with_retry(t)
        if entry is not None:
            rows.append((t, entry))

    llm.chat.completions.create = orig


    print(" RESULTS ")
    print(f"{'film review':<40} | {'title':<14} | {'rating':<6} | {'sentiment'}")

    for text, e in rows:
        short = text if len(text) <= 39 else text[:36] + "..."
        print(f"{short:<40} | {e['title']:<14} | {e['rating']:<6} | {e['sentiment']}")


    pos = len([r for r in rows if r[1]["sentiment"] == "positive"])
    neg = len(rows) - pos
    print(f"  positive: {pos}   negative: {neg}")

    return rows


# ---------------------------------------------------------------------------
# temperature check (bonus)
# ---------------------------------------------------------------------------
def compare(data):
    """run once at temp=0 and once at temp=1.5, count retries + failures"""
    orig_create = llm.chat.completions.create
    orig_ask = ask_llm

    for temp_value in (0.0, 1.5):
        llm.chat.completions.create = lambda *a, **kw: orig_create(*a, **{**kw, "temperature": temp_value})

        counter = {"n": 0}

        def wrapper(prompt, system, _c=counter):
            _c["n"] += 1
            return orig_ask(prompt, system)

        ask_llm.__globals__["ask_llm"] = wrapper

        failed = 0
        retried = 0
        for sample_text in data:
            counter["n"] = 0
            res = extract_with_retry(sample_text)
            if res is None:
                failed += 1
            elif counter["n"] > 1:
                retried += 1

        print(f"  temp={temp_value}: retries={retried} failures={failed}")

    ask_llm.__globals__["ask_llm"] = orig_ask
    llm.chat.completions.create = orig_create


if __name__ == "__main__":
    process(TEXTS)
    compare(TEXTS)
