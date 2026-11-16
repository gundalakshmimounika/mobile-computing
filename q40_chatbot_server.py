# Program 40 - Chatbot with TF-IDF + cosine similarity (Flask service)
# Install: pip install flask scikit-learn
# Run:     python q40_chatbot_server.py     -> prints the sample test table, then starts the server on port 5001
from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

INTENTS = [
    (["hello", "hi there", "good morning", "hey"], "Hello! How can I help you with mobile computing?"),
    (["what is handoff", "explain handover", "cell change during call"],
     "Handoff transfers an ongoing call from one cell to another as the user moves."),
    (["what is gsm", "tell me about gsm"], "GSM is a 2G TDMA/FDMA digital cellular standard."),
    (["what is mobile ip", "care of address", "home agent"],
     "Mobile IP lets a node keep its home address while moving; a home agent tunnels packets to its care-of address."),
    (["difference between aodv and dsdv", "reactive and proactive routing"],
     "DSDV is proactive (tables kept up to date); AODV is reactive (routes discovered on demand)."),
    (["bye", "goodbye", "see you"], "Goodbye! Happy learning."),
]
FALLBACK = "Sorry, I did not understand. Try asking about handoff, GSM or Mobile IP."

patterns, replies = [], []
for pats, rep in INTENTS:
    for p in pats:
        patterns.append(p)
        replies.append(rep)

vec = TfidfVectorizer(ngram_range=(1, 2), stop_words="english", lowercase=True)
X = vec.fit_transform(patterns)


def answer(msg):
    sims = cosine_similarity(vec.transform([msg]), X)[0]
    best = sims.argmax()
    return (replies[best] if sims[best] >= 0.35 else FALLBACK), float(sims[best])


app = Flask(__name__)


@app.post("/chat")
def chat():
    msg = (request.get_json() or {}).get("message", "").strip()
    if not msg:
        return jsonify(reply="Please type something.")
    reply, score = answer(msg)
    return jsonify(reply=reply, score=score)


if __name__ == "__main__":
    print("\nProgram 40 - Chatbot test")
    print("-" * 70)
    for m in ["hi", "what is handover", "explain mobile ip", "what is the weather"]:
        r, s = answer(m)
        print(f"User: {m:<22} Bot: {r}  (score {s:.2f})")
    print("\nServer running at http://127.0.0.1:5001/chat  (Ctrl+C to stop)")
    app.run(host="0.0.0.0", port=5001)
