from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

# ハンバーガーメニュー内の既存「支援」リンクを正規化し、なければ Search と Home の間に追加します。
# root配下のHTML: donate.html
# audit/ などサブディレクトリ配下のHTML: ../donate.html

MOBILE_SUPPORT_RE = re.compile(
    r'\n?\s*<a\s+class="mobile-link(?:\s+mobile-link--support)?"\s+href="[^"]*donate(?:/index)?\.html"\s*>\s*<span>Support</span>支援\s*</a>',
    re.I,
)
SEARCH_LINK_RE = re.compile(
    r'(<a\s+class="mobile-link"\s+href="[^"]*search\.html"\s*>\s*<span>Search</span>検索\s*</a>)',
    re.I,
)
HOME_LINK_RE = re.compile(
    r'(<a\s+class="mobile-link"\s+href="[^"]*index\.html"\s*>\s*<span>Home</span>トップ\s*</a>)',
    re.I,
)
MOBILE_GROUP_RE = re.compile(r'(<div\s+class="mobile-group"[^>]*>.*?</div>\s*<div\s+class="close-overlay")', re.I | re.S)

# トップの上部ボタンにも「支援する」を足す。不要なら PATCH_HOME_ACTIONS = False にしてください。
PATCH_HOME_ACTIONS = True
HOME_ACTIONS_RE = re.compile(r'(<div\s+class="home-actions"[^>]*>)(.*?)(</div>)', re.I | re.S)
BOARD_BTN_RE = re.compile(r'(<a\s+class="home-btn"\s+href="guide-board\.html">学校・教育委員会</a>)')

# 任意：上部デスクトップナビにも「支援」を足す。不要なら PATCH_DESKTOP_NAV = False にしてください。
PATCH_DESKTOP_NAV = True
DESKTOP_DONATE_RE = re.compile(r'<a\s+class="nav-link"\s+href="[^"]*donate\.html"\s*>支援</a>', re.I)
SEARCH_NAV_RE = re.compile(r'(<a\s+class="nav-link"\s+href="[^"]*search\.html"\s*>検索</a>)', re.I)
ARCHIVE_NAV_RE = re.compile(r'(<a\s+class="nav-link"\s+href="[^"]*archive\.html"\s*>資料</a>)', re.I)


def rel_prefix(path: Path) -> str:
    parent = path.parent.relative_to(ROOT)
    if str(parent) == '.':
        return ''
    return '../' * len(parent.parts)


def patch_mobile(text: str, href: str):
    support = f'<a class="mobile-link mobile-link--support" href="{href}"><span>Support</span>支援</a>'
    # まず既存の支援リンクを削除してから入れ直し、重複とパス誤りを防ぐ。
    text2 = MOBILE_SUPPORT_RE.sub('', text)
    def patch_group(m):
        block = m.group(1)
        if support in block:
            return block
        if SEARCH_LINK_RE.search(block):
            block = SEARCH_LINK_RE.sub(r'\1\n' + support, block, count=1)
        elif HOME_LINK_RE.search(block):
            block = HOME_LINK_RE.sub(support + r'\n\1', block, count=1)
        else:
            # mobile-group はあるが Search/Home がない場合は末尾寄りへ追加
            block = block.replace('</div>\n<div class="close-overlay"', support + '\n</div>\n<div class="close-overlay"', 1)
        return block
    text3 = MOBILE_GROUP_RE.sub(patch_group, text2, count=1)
    return text3


def patch_home_actions(text: str):
    if 'href="donate.html">支援する</a>' in text:
        return text
    def repl(m):
        inner = m.group(2)
        if 'donate.html' in inner or '支援する' in inner:
            return m.group(0)
        if BOARD_BTN_RE.search(inner):
            inner = BOARD_BTN_RE.sub(r'\1\n  <a class="home-btn" href="donate.html">支援する</a>', inner, count=1)
        else:
            inner = inner + '\n  <a class="home-btn" href="donate.html">支援する</a>\n'
        return m.group(1) + inner + m.group(3)
    return HOME_ACTIONS_RE.sub(repl, text, count=1)


def patch_desktop_nav(text: str, href: str):
    if DESKTOP_DONATE_RE.search(text):
        return text
    donate_link = f'<a class="nav-link" href="{href}">支援</a>'
    if SEARCH_NAV_RE.search(text):
        return SEARCH_NAV_RE.sub(donate_link + '\n' + r'\1', text, count=1)
    if ARCHIVE_NAV_RE.search(text):
        return ARCHIVE_NAV_RE.sub(r'\1' + '\n' + donate_link, text, count=1)
    return text


def main():
    changed = []
    skipped = []
    for path in sorted(ROOT.rglob('*.html')):
        rel = path.relative_to(ROOT).as_posix()
        if rel in {'donate.html', 'donate/index.html'}:
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            skipped.append((rel, 'encoding'))
            continue
        prefix = rel_prefix(path)
        href = prefix + 'donate.html'
        new = text
        if 'mobile-overlay' in new and 'mobile-group' in new:
            new = patch_mobile(new, href)
        else:
            skipped.append((rel, 'no mobile menu'))
        if PATCH_DESKTOP_NAV and '<nav' in new and 'desktop-nav' in new:
            new = patch_desktop_nav(new, href)
        if PATCH_HOME_ACTIONS and rel == 'index.html':
            new = patch_home_actions(new)
        if new != text:
            path.write_text(new, encoding='utf-8')
            changed.append(rel)
    log = ['PTA donate/support patch result', '', 'Updated files:']
    log += [f'- {x}' for x in changed] or ['(none)']
    log += ['', 'Skipped files:']
    log += [f'- {p}: {why}' for p, why in skipped] or ['(none)']
    (ROOT / 'patch_donate_support_result.txt').write_text('\n'.join(log) + '\n', encoding='utf-8')
    print('\n'.join(log))

if __name__ == '__main__':
    main()
