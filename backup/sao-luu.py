"""Sao lưu toàn bộ collection `replies` từ Firestore ra file JSON trong repo."""
import json, urllib.request, datetime, os, sys

PROJECT = "ky-anh-studio---reply-d43ff"
URL = (f"https://firestore.googleapis.com/v1/projects/{PROJECT}"
       "/databases/(default)/documents/replies?pageSize=300")
HERE = os.path.dirname(os.path.abspath(__file__))

# Mac dinh: ghi de replies-backup.json ngay canh script (ban trong repo).
# Them "--ra <thu muc>": luu ra cho khac, dat ten kem ngay gio va giu lai
# nhieu ban — dung cho sao luu tu dong dinh ky.
RA_NGOAI = None
if "--ra" in sys.argv:
    RA_NGOAI = sys.argv[sys.argv.index("--ra") + 1]

if RA_NGOAI:
    moc = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    OUT = os.path.join(RA_NGOAI, f"replies-{moc}.json")
else:
    OUT = os.path.join(HERE, "replies-backup.json")


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

if RA_NGOAI:
    # Giu 12 ban gan nhat, xoa dan ban cu hon cho khoi day o dia
    cu = sorted(f for f in os.listdir(RA_NGOAI)
                if f.startswith("replies-") and f.endswith(".json"))
    for f in cu[:-12]:
        os.remove(os.path.join(RA_NGOAI, f))
        print(f"  don ban cu: {f}")

    # Sao luu them sheet concept (tab Concept cua app doc thang tu Google Sheet nay).
    # Sheet ma loi (#REF!) thi KHONG luu, de ban tot gan nhat khong bi day ra khoi 12 ban.
    SHEET = ("https://docs.google.com/spreadsheets/d/"
             "1xhYHsQDVgUaIzj8_i0wBFDqa5k7OsUjPqgVc-Jn2CaE/export?format=csv")
    try:
        with urllib.request.urlopen(SHEET) as r:
            csv_text = r.read().decode("utf-8")
        so_dong = sum(1 for d in csv_text.splitlines() if d.strip(", \t"))
        if csv_text.lstrip().startswith("#") or so_dong < 5:
            print(f"CANH BAO: sheet concept dang loi ({csv_text.strip()[:30]!r}) — khong luu, giu ban cu.")
        else:
            ra = os.path.join(RA_NGOAI, f"concept-{moc}.csv")
            with open(ra, "w", encoding="utf-8-sig", newline="") as f:
                f.write(csv_text)
            print(f"Da sao luu sheet concept ({so_dong - 1} dong) -> {ra}")
            cu = sorted(f for f in os.listdir(RA_NGOAI)
                        if f.startswith("concept-") and f.endswith(".csv"))
            for f in cu[:-12]:
                os.remove(os.path.join(RA_NGOAI, f))
                print(f"  don ban cu: {f}")
    except Exception as e:
        print(f"CANH BAO: khong tai duoc sheet concept ({e}) — bo qua, mau tra loi van da luu.")
