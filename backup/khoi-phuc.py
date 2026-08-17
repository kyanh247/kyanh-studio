"""
KHOI PHUC mau tra loi tu file backup len Firestore.

Cach dung (mo Terminal tai thu muc kyanh-studio):
    python backup/khoi-phuc.py          -> chi xem truoc, KHONG ghi gi
    python backup/khoi-phuc.py --that   -> ghi that len Firebase

Chi nap lai nhung mau DA MAT. Mau nao con tren Firebase thi giu nguyen,
khong ghi de -> chay nham cung khong lam hong du lieu dang co.
"""
import json, os, sys, urllib.request, urllib.error

PROJECT = "ky-anh-studio---reply-d43ff"
PIN = "794831"  # phai khop KA_ADMIN_PIN trong index.html
BASE = (f"https://firestore.googleapis.com/v1/projects/{PROJECT}"
        "/databases/(default)/documents/replies")
BACKUP = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "replies-backup.json")
THAT = "--that" in sys.argv


def typed(v):
    if isinstance(v, bool):
        return {"booleanValue": v}
    if isinstance(v, int):
        return {"integerValue": str(v)}
    if isinstance(v, float):
        return {"doubleValue": v}
    if v is None:
        return {"nullValue": None}
    return {"stringValue": str(v)}


def get_json(url):
    with urllib.request.urlopen(url) as r:
        return json.load(r)


data = json.load(open(BACKUP, encoding="utf-8"))
items = data["items"]
print(f"File backup: {data['count']} mau, luu luc {data['backed_up_at']}\n")

# Lay danh sach ID dang co tren Firebase
dang_co, url = set(), BASE + "?pageSize=300"
while url:
    page = get_json(url)
    for d in page.get("documents", []):
        dang_co.add(d["name"].split("/")[-1])
    tok = page.get("nextPageToken")
    url = BASE + "?pageSize=300&pageToken=" + tok if tok else None

thieu = [it for it in items if it["_id"] not in dang_co]
print(f"Tren Firebase dang co : {len(dang_co)} mau")
print(f"Mau bi mat can nap lai: {len(thieu)}\n")

if not thieu:
    print("Khong co gi de khoi phuc — du lieu con nguyen.")
    sys.exit()

for it in thieu:
    print("  -", it.get("cat"), "|", it.get("title"))

if not THAT:
    print("\n(Moi chi xem truoc. Chay lai voi --that de nap len Firebase.)")
    sys.exit()

print("\nDang nap len Firebase...")
ok = loi = 0
for it in thieu:
    doc_id = it["_id"]
    fields = {k: typed(v) for k, v in it.items() if k != "_id"}
    fields["_key"] = {"stringValue": PIN}
    req = urllib.request.Request(
        f"{BASE}?documentId={doc_id}",
        data=json.dumps({"fields": fields}).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        urllib.request.urlopen(req)
        ok += 1
    except urllib.error.HTTPError as e:
        loi += 1
        print(f"  LOI {it.get('title')}: {e.code} {e.read()[:200]}")

print(f"\nXong: nap lai {ok} mau" + (f", {loi} mau loi" if loi else ""))
