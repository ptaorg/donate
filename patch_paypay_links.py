from pathlib import Path

NEW_PAYPAY = "https://qr.paypay.ne.jp/p2p01_7qyY46XqZxGgVsQw"
KNOWN_OLD_PAYPAY_URLS = ['https://qr.paypay.ne.jp/p2p01_OOcoe73WXQOj8C9p', 'https://qr.paypay.ne.jp/p2p01_G9Jr8B9j01wcCN0u', 'https://qr.paypay.ne.jp/p2p01_C2WQJYLTMuGv3hmV']

updated = []
for html in Path(".").rglob("*.html"):
    if ".git" in html.parts:
        continue
    text = html.read_text(encoding="utf-8", errors="ignore")
    before = text
    for old in KNOWN_OLD_PAYPAY_URLS:
        text = text.replace(old, NEW_PAYPAY)
    if text != before:
        html.write_text(text, encoding="utf-8")
        updated.append(str(html))

print("PayPayリンク差し替え完了")
print("更新ファイル数:", len(updated))
for name in updated:
    print("-", name)
