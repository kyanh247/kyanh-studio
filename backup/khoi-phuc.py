"""
KHOI PHUC mau tra loi tu file backup len Firestore.

Cach dung (mo Terminal tai thu muc kyanh-studio):
    python backup/khoi-phuc.py          -> chi xem truoc, KHONG ghi gi
    python backup/khoi-phuc.py --that   -> dang nhap roi ghi that len Firebase

Chi nap lai nhung mau DA MAT. Mau nao con tren Firebase thi giu nguyen,
khong ghi de -> chay nham cung khong lam hong du lieu dang co.

Tu 21/08/2026 script dang nhap bang EMAIL + MAT KHAU quan tri (Firebase Auth).
Cach cu ghi kem _key = PIN da bi Firestore Rules chan, khong dung duoc nua.
"""
import json, os, re, sys, getpass, urllib.request, urllib.error

PROJECT = "ky-anh-studio---reply-d43ff"
BASE = (f"https://firestore.googleapis.com/v1/projects/{PROJECT}"
        "/databases/(default)/documents/replies")
HERE = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(HERE, "replies-backup.json")
THAT = "--that" in sys.argv


def doc_api_key():
    """Lay apiKey tu index.html o goc repo — de chi phai sua mot cho khi doi project.

    apiKey cua Firebase von la thong tin cong khai (no nam san trong trang web),
    cai bao ve du lieu la Firestore Rules chu khong phai giau key nay.
    """
    idx = os.path.join(HERE, "..", "index.html")
    try:
        with open(idx, encoding="utf-8") as f:
            m = re.search(r'apiKey:\s*"([^"]+)"', f.read())
        if m:
            return m.group(1)
    except OSError:
        pass
    sys.exit("KHONG doc duoc apiKey trong index.html — kiem tra lai file.")


def post_json(url, payload, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers=headers, method="POST")
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def dang_nhap():
    """Doi email/mat khau quan tri lay ve idToken de ghi Firestore."""
    key = doc_api_key()
    print("Dang nhap bang tai khoan quan tri (email da them trong Firebase Console)")
    email = input("  Email    : ").strip()
    matkhau = getpass.getpass("  Mat khau : ")
    url = ("https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
           f"?key={key}")
    try:
        res = post_json(url, {"email": email, "password": matkhau,
                              "returnSecureToken": True})
    except urllib.error.HTTPError as e:
        loi = json.load(e).get("error", {}).get("message", "?")
        sys.exit(f"\nDang nhap that bai: {loi}\n"
                 "  EMAIL_NOT_FOUND / INVALID_LOGIN_CREDENTIALS -> sai email hoac mat khau\n"
                 "  CONFIGURATION_NOT_FOUND -> chua bat Email/Password trong Firebase Console")
    print(f"  OK — dang nhap voi {res['email']}\n")
    return res["idToken"]


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

# Lay danh sach ID dang co tren Firebase (doc khong can dang nhap)
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

token = dang_nhap()

print("Dang nap len Firebase...")
ok = loi = 0
for it in thieu:
    doc_id = it["_id"]
    fields = {k: typed(v) for k, v in it.items() if k != "_id"}
    try:
        post_json(f"{BASE}?documentId={doc_id}", {"fields": fields}, token)
        ok += 1
    except urllib.error.HTTPError as e:
        loi += 1
        print(f"  LOI {it.get('title')}: {e.code} {e.read()[:200]}")

print(f"\nXong: nap lai {ok} mau" + (f", {loi} mau loi" if loi else ""))
