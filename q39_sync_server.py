# Program 39 - Flask web service for two-way sync (last-write-wins)
# Run:  python q39_sync_server.py      (keep it running; then run q39_sync_demo_client.py in a 2nd terminal)
# Install: pip install flask
from flask import Flask, request, jsonify

app = Flask(__name__)
notes = {}                                   # id -> {id, text, updatedAt}


@app.post("/notes")
def push():
    n = request.get_json()
    old = notes.get(n["id"])
    if old is None or n["updatedAt"] >= old["updatedAt"]:      # last-write-wins
        notes[n["id"]] = n
    print("POST /notes ->", n)
    return jsonify(ok=True)


@app.get("/notes")
def pull():
    since = int(request.args.get("since", 0))
    print("GET /notes?since=%d" % since)
    return jsonify([n for n in notes.values() if n["updatedAt"] > since])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
