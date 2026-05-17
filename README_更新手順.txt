PTA適正化推進委員会 PayPayリンク差し替え版

内容:
- 新PayPay URL: https://qr.paypay.ne.jp/p2p01_7qyY46XqZxGgVsQw
- donate.html のPayPayボタンと代替表示URLを差し替え済みです。
- donate/index.html は donate.html へ転送する補助ページです。
- patch_paypay_links.py は既存サイト内の古いPayPayリンクを新URLへ一括置換する補助スクリプトです。

使い方:
1. ZIPを展開します。
2. 既存サイトのルートに donate.html と donate/ を上書き配置します。
3. 既存サイト全体の古いPayPayリンクも置換したい場合は、既存サイトのルートで patch_paypay_links.py を実行します。

注意:
PayPayの個人送金リンク／QRは期限切れになる場合があります。期限切れ時はPayPayアプリで新しいリンクを取得し、このURLを再度差し替えてください。
