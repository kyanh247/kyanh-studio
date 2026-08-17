"""Sao lưu toàn bộ collection `replies` từ Firestore ra file JSON trong repo."""
import json, urllib.request, datetime, os, sys

PROJECT = "ky-anh-studio---reply-d43ff"
URL = (f"https://firestore.googleapis.com/v1/projects/{PROJECT}"
       "/databases/(default)/documents/replies?pageSize=300")
OUT = r"G:\KAS-AllApp\KYANH.STUDIO\kyanh-studio\backup\replies-backup.json"


def untype(v):
    """Đổi kiểu dữ liệu rườm rà của Firestore về JSON thường."""
    if "stringValue" in v:
        return v["stringValue"]
    if "integerValue" in v:
        return int(v["integerValue"])
    if "doubleValue" in v:
        return v["doubleValue"]
    if "booleanValue" in v:
        return v["booleanValue"]
    if "nullValue" in v:
        return None
    if "arrayValue" in v:
        return [untype(x) for x in v["arrayValue"].get("values", [])]
    if "mapValue" in v:
        return {k: untype(x) for k, x in v["mapValue"].get("fields", {}).items()}
    return v


docs = []
url = URL
while url:
    with urllib.request.urlopen(url) as r:
        page = json.load(r)
    for d in page.get("documents", []):
        # Bo _key (ma PIN) — script khoi phuc tu gan lai, khong can luu them mot ban
        item = {k: untype(v) for k, v in d.get("fields", {}).items() if k != "_key"}
        item["_id"] = d["name"].split("/")[-1]
        docs.append(item)
    token = page.get("nextPageToken")
    url = URL + "&pageToken=" + token if token else None

if not docs:
    sys.exit("KHONG lay duoc mau nao — huy, khong ghi de backup cu.")

docs.sort(key=lambda x: x.get("order", 0))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
payload = {
    "backed_up_at": datetime.datetime.now().isoformat(timespec="seconds"),
    "project": PROJECT,
    "collection": "replies",
    "count": len(docs),
    "items": docs,
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print(f"Da sao luu {len(docs)} mau -> {OUT}")
