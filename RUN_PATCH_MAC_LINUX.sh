#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
python3 patch_donate_support_links.py
echo
echo "完了しました。patch_donate_support_result.txt を確認してください。"
