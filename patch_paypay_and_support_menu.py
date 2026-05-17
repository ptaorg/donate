from pathlib import Path
import re

ROOT = Path(".")
OLD_PAYPAY = "https://qr.paypay.ne.jp/" + "p2p01_" + "OOcoe73" + "WXQOj8C9p"
NEW_PAYPAY = "https://qr.paypay.ne.jp/p2p01_G9Jr8B9j01wcCN0u"

def depth_prefix(path: Path) -> str:
    depth = len(path.parent.parts)
    return "../" * depth

changed = []
for html in ROOT.rglob("*.html"):
    if ".git" in html.parts:
        continue
    s = html.read_text(encoding="utf-8", errors="ignore")
    original = s

    s = s.replace(OLD_PAYPAY + " ", NEW_PAYPAY)
    s = s.replace(OLD_PAYPAY, NEW_PAYPAY)

    if 'class="mobile-group"' in s and 'mobile-link--support' not in s:
        prefix = depth_prefix(html)
        href = f"{prefix}donate.html"
        support_link = f'<a class="mobile-link mobile-link--support" href="{href}"><span>Support</span>支援</a>\n'
        s2 = re.sub(
            r'(<a class="mobile-link" href="(?:\.\./)*index\.html"><span>Home</span>トップ</a>)',
            support_link + r'\1',
            s,
            count=1
        )
        if s2 == s:
            s2 = re.sub(
                r'(<a class="mobile-link" href="(?:\.\./)*search\.html"><span>Search</span>検索</a>\s*)',
                r'\1' + support_link,
                s,
                count=1
            )
        if s2 == s:
            s2 = s.replace('</div>\n<div class="close-overlay"', support_link + '</div>\n<div class="close-overlay"', 1)
        s = s2

    if 'class="desktop-nav desktop-nav--simple"' in s and '>支援</a>' not in s:
        prefix = depth_prefix(html)
        href = f"{prefix}donate.html"
        nav_link = f'<a class="nav-link" href="{href}">支援</a>\n'
        s = re.sub(
            r'(<a class="nav-link" href="(?:\.\./)*search\.html">検索</a>\s*)',
            r'\1' + nav_link,
            s,
            count=1
        )

    if s != original:
        html.write_text(s, encoding="utf-8")
        changed.append(str(html))

print("更新ファイル数:", len(changed))
for p in changed:
    print("-", p)
