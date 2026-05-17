これは「支援ページ donate.html」と「ハンバーガーメニューの支援リンク」を既存サイトに組み込むための実適用パッチZIPです。

前回版の問題:
- ハンバーガーメニュー用のHTML断片だけを入れており、既存の index.html 等を実際に書き換えていませんでした。

今回版で行うこと:
1. donate.html をルート直下へ配置します。
2. donate/index.html を追加し、/donate/ でも donate.html に転送されるようにします。
3. patch_donate_support_links.py を実行すると、既存サイト内の各HTMLのハンバーガーメニューに「支援」を追加します。
4. index.html のトップボタン列にも「支援する」を追加します。
5. 上部デスクトップナビにも「支援」を追加します。

使い方:
1. このZIPを、既存サイトのルートフォルダで展開してください。
   例: index.html / css / js / assets があるフォルダです。
2. Windowsなら RUN_PATCH_WINDOWS.bat をダブルクリック。
   Mac/Linuxなら RUN_PATCH_MAC_LINUX.sh を実行。
3. patch_donate_support_result.txt に更新されたHTML一覧が出ます。
4. 更新後のフォルダをZIP化してGitHubへアップロードしてください。

注意:
- donate.html は、提供されたHTML本文に基づいています。
- PayPayリンクの href 末尾に半角スペースが入っていたため、その空白だけ除去しています。
- 銀行口座・PayPayリンク等の内容確認は、提供本文どおりです。


【更新】
PayPayリンクを以下に差し替え済みです。
https://qr.paypay.ne.jp/p2p01_G9Jr8B9j01wcCN0u
