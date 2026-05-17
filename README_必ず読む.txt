PTA適正化推進委員会 donate.html 修正版

内容:
1. donate.html
   - PayPayリンクを新URLに差し替え済み
   - 新URL: https://qr.paypay.ne.jp/p2p01_G9Jr8B9j01wcCN0u

2. donate/index.html
   - /donate/ から donate.html へ転送する補助ページ

3. patch_paypay_and_support_menu.py
   - 既存サイト内の *.html を走査し、以下を実施します。
     a. 古いPayPayリンクを新PayPayリンクへ置換
     b. ハンバーガーメニューに「支援」を追加
     c. 上部ナビに「支援」を追加

使い方:
- 既存サイトの index.html があるフォルダに、このZIPの中身を上書き展開してください。
- Windows: RUN_PATCH_WINDOWS.bat を実行
- Mac/Linux: RUN_PATCH_MAC_LINUX.sh を実行
