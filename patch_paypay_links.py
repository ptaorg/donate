from pathlib import Path
import re

ROOT = Path(".")
NEW_PAYPAY = "https://qr.paypay.ne.jp/p2p01_C2WQJYLTMuGv3hmV"
KNOWN_OLD_PAYPAY_URLS = ['https://qr.paypay.ne.jp/p2p01_OOcoe73WXQOj8C9p', 'https://qr.paypay.ne.jp/p2p01_G9Jr8B9j01wcCN0u']

# PayPay P2P QR URL only. Other PayPay-related text is not touched.
P2P_PATTERN = re.compile(r"https://qr\.paypay\.ne\.jp/p2p01_[A-Za-z0-9]+")

changed = []
for html in ROOT.rglob("*.html"):
    if ".git" in html.parts:
        continue
    text = html.read_text(encoding="utf-8", errors="ignore")
    original = text

    text = P2P_PATTERN.sub(NEW_PAYPAY, text)

    if text != original:
        html.write_text(text, encoding="utf-8")
        changed.append(str(html))

print("PayPayリンク更新ファイル数:", len(changed))
for path in changed:
    print("-", path)
print("新PayPay URL:", NEW_PAYPAY)
