PTA適正化推進委員会 PayPayリンク修正版

更新内容
- donate.html のPayPayリンクを新URLへ差し替えました。
- 新PayPay URL: https://qr.paypay.ne.jp/p2p01_C2WQJYLTMuGv3hmV
- ボタンが開かない場合のため、同じURLを本文にも表示しています。
- /donate/ で開いた場合も donate.html へ転送する donate/index.html を同梱しています。

既存サイトへの反映方法
1. このZIPを既存サイトのルート、つまり index.html がある場所へ展開してください。
2. donate.html と donate/index.html を上書きしてください。
3. 既存ページ内に古いPayPayリンクが残っている可能性がある場合は、同じ場所で patch_paypay_links.py を実行してください。
   - Windows: RUN_PATCH_WINDOWS.bat
   - Mac/Linux: RUN_PATCH_MAC_LINUX.sh

確認済み事項
- donate.html 内のPayPayリンクは、指定された新URLだけです。
- href属性内に余計な空白や改行は入れていません。
