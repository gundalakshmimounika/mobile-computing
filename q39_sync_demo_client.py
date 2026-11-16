
import json
import time
import urllib.request

BASE = "http://127.0.0.1:5000"


def post(note):
    req = urllib.request.Request(BASE + "/notes", data=json.dumps(note).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    return urllib.request.urlopen(req).status


def get(since):
    return json.loads(urllib.request.urlopen(f"{BASE}/notes?since={since}").read())


class Device:
    def __init__(self, name):
        self.name, self.db, self.last = name, {}, 0      # db: id -> note(+synced)

    def edit(self, nid, text, ts=None):                   # offline edit -> synced = False
        self.db[nid] = {"id": nid, "text": text, "updatedAt": ts or int(time.time() * 1000), "synced": False}
        print(f"[{self.name}] edit '{text}' saved locally, synced=False")

    def sync(self):                                       # push then pull
        for n in [x for x in self.db.values() if not x["synced"]]:
            if post({k: n[k] for k in ("id", "text", "updatedAt")}) == 200:
                n["synced"] = True
        for n in get(self.last):
            self.db[n["id"]] = {**n, "synced": True}
        self.last = int(time.time() * 1000)
        print(f"[{self.name}] synced -> {[(v['text']) for v in self.db.values()]}")


A, B = Device("Phone-A"), Device("Phone-B")

print("\n1) Create a note offline on A")
A.edit("n1", "Buy SIM card", ts=1000)
print("\n2) Reconnect: A pushes")
A.sync()
print("\n3) B syncs and receives the note")
B.sync()
print("\n4) Conflicting edits: A edits at t=2000, B edits at t=3000 (offline)")
A.edit("n1", "Buy SIM card (A)", ts=2000)
B.edit("n1", "Buy SIM card (B)", ts=3000)
A.sync(); B.sync(); A.sync()
print("\nResult: latest updatedAt wins ->", A.db["n1"]["text"])
