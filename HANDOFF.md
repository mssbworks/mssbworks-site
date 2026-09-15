# HANDOFF: mssbworks コーポレートサイト

2026-09-15 更新。このファイルだけ読めば再開できることを目標にした引き継ぎ。
元になったセッション「mssbworks corporate site」は2026-07-03で止まっている。
そのあと2026-08-21〜09-07に別のセッションから手が入っているので、
**セッションの記録より、このファイルとgitログを信じること。**

## 現在地

- サイトは公開中。<https://mssbworks.com> を **GitHub Pages** が配信している
- 1ページ縦スクロールのトップ＋下層2ページ（`/muku/` `/privacy/`）
- 手元の `~/mssb/website` と本番は、2026-09-15時点で全14ファイルの指紋が一致している
  （`.cloudflare/検収.py` で確認済み）
- 最後のコミットは2026-09-07 11:23 `0170236 取っていないものの列挙をやめた`。
  `origin/main` にpush済みで、未pushのものは無い
- Cloudflare Workers版（`mssbworks-site`）は2026-09-04に一度デプロイされたまま生きているが、
  **中身が9月4日で止まっている。本番のドメインには繋がっていない**（後述）

## 構成

| ファイル | 中身 |
|---|---|
| `index.html` | トップ。第一声／Philosophy／写真／Vision／Mission／Values／BUSINESS／WORKS／二つの窓（問い合わせ）／会社情報 |
| `muku/index.html` | 飲食店向けAIスキル「ムク」のページ。改修のお知らせ登録フォームと、`#help` の窓口フォーム |
| `privacy/index.html` | プライバシーポリシー（2026年9月6日制定） |
| `style.css` | 全ページ共通。`:root` にトークン。下層ページの体裁だけ各HTMLの `<style>` に置いてある |
| `img/` | 写真・ロゴ・OG画像・favicon |
| `apple-touch-icon*.png` | ホーム画面アイコン。サイト直下にも置く（iOSが拾わないことがあるため） |
| `CNAME` | `mssbworks.com`。GitHub Pagesの独自ドメイン指定。**消すと本番のドメインが外れる** |
| `wrangler.jsonc` `.assetsignore` `.cloudflare/検収.py` | Cloudflare関係。いまは検収スクリプトだけが現役 |

トップに `id` の付いたセクションは無く、ナビゲーションも無い。深いリンクは `#contact` と
`/muku/#help` の2つだけで、どちらもJavaScriptが位置まで連れていく作りになっている。

## 公開の手順

```bash
cd ~/mssb/website
git add -A && git commit -m "……"
git push                      # origin = git@github.com:mssbworks/mssbworks-site.git
```

push すると GitHub Pages が main ブランチの直下をそのまま公開する。ビルドは無い。
反映まで1〜2分。そのあと必ず検収する。

```bash
cd ~/mssb/website
python3 .cloudflare/検収.py https://mssbworks.com
```

全ファイルのSHA-256を突き合わせて「全◯本が指紋まで一致」と出れば終わり。
**目視で「だいたい同じ」にしない。**キャッシュで古いものが見えることがある。

## ドメインとDNS

| 役割 | どこ |
|---|---|
| ドメイン登録 | Wix。更新期限は2027年6月3日 |
| DNS | Wix（`ns12/ns13.wixdns.net`）。**Wixの仕様でネームサーバーを変更できない** |
| サイト配信 | GitHub Pages（Aレコード4本 `185.199.108-111.153`、`www` は `mssbworks.github.io.`） |
| メール受信 | Google Workspace。MXが5本ある |
| 問い合わせ | Web3Forms（メール通知）＋ Cloudflare Worker `muku-mcp`（D1に記録）の並走 |

実測の全レコード表は `~/mssb/_company/dns_cloudflare移行_20260904.md` にある。
**DNSを触るときは必ずその表と突き合わせる。MXを1件でも落とすとメールが止まる。**

## 決定済みの事項

- **DNSはWixに置いたままにする**（2026-09-05）。理由: Wixドメインはネームサーバーを変更できず、
  Cloudflare Registrarへの移管も「先にCloudflareのNSで動いていること」が条件で循環する。
  別レジストラを1回挟む2段構えになり、その間メールが止まる恐れがある。釣り合わない
- **サイトのWorkers移行は保留**（2026-09-05）。理由: Workersのカスタムドメインにはゾーンが要る。
  DNSを移せない以上できない。GitHub Pagesで動いていて困っていない
- Cloudflare側のゾーン（`mssbworks.com`・Free・12レコード読み込み済み）は**pendingのまま残す**。
  無害で、気が変わればすぐ使える
- **問い合わせフォームはWeb3FormsとうちのWorkerの並走のまま据え置く**（2026-09-05、A案）。
  理由: Web3Formsを切るとメール通知が消えて、問い合わせが来ても気づけない。
  CloudflareからメールをHTMLで送るにはWorkersの有料プラン（月5ドル・年約9,000円）が要る。
  無料で預け先を減らす道は無い。見送った案 = B案（有料プランでWeb3Formsを切る）
- **画面の成否はWeb3Forms側だけで決める**（2026-09-05）。Workerへの控え送信が落ちても
  問い合わせが送れなくなってはいけないので、失敗は握りつぶしてコンソールにだけ出す
- Netlifyはやめた（2026-06-30）。Netlify Forms依存を外してWeb3Forms化し、`netlify.toml` を削除した
- ムクのページを `/muku/` に追加（2026-09-01）。窓口を同じページの `#help` に置いた（2026-09-05）。
  理由: ムクが「数字が合わなかったらここへ」と出す先が要る。トップの問い合わせ窓とは分ける
- プライバシーポリシーを `/privacy/` に作った（2026-09-06）。翌日「取っていないものの列挙」をやめた。
  理由: 取っていないものを並べると、かえって何を取っているのか分かりにくくなる

## ルールと地雷

- ⚠️ **本文テキストを勝手に書かない。**このサイトの立ち上げからの絶対ルール。
  見出し以外の文章は渡部が入れる。空欄はプレースホルダで残す
- ⚠️ **`CNAME` を消さない。**消すと独自ドメインの設定がGitHub側から外れる
- ⚠️ **`wrangler deploy` はディレクトリを丸ごと読む。**2026-09-04に13ファイルのつもりが
  214ファイル上がり、`.git/config` が公開URLで取れる状態になった。
  `.assetsignore` が効いていることを、実際に `/.git/config` を叩いて404で確かめること
  （2026-09-15時点では404で塞がっている）
- ⚠️ **除外リストを2箇所に書かない。**`.assetsignore` が正本で、検収スクリプトはそれを読む。
  二重管理にすると検収が嘘をつく（2026-09-04に実際に出た）
- **リポジトリは public。**秘密になるものをコミットしない。
  HTMLに入っている Web3Forms の `access_key` は公開前提の鍵なのでこれは問題ない
- ムクのページのフォームは2つある（お知らせ登録／窓口）。`querySelectorAll` で両方を拾っている。
  **`querySelector` に変えない。**足したフォームが黙って動かない形の事故になる
- 深いリンクをなめらかスクロールにしない。フォームはページの8,000px下にあり、途中で止まる
  （2026-09-05に実際に止まった）
- `#contact` から来たときは `source` を `'contact'` にする。`'work'` や `'create'` のままだと、
  不具合の報告が「仕事の相談」として記録される
- 画面の見た目を変えたら、狭い幅（スマホ）でも見ること。このサイトは立ち上げから
  スマホでの見え方で何度も差し戻しになっている

## 次にやること（上から着手順）

1. **Cloudflare Workers版を止めるか、上げ直すか決める。**
   `https://mssbworks-site.muku-mcp.workers.dev/` がまだ生きていて、中身が2026-09-04のまま。
   `/privacy/` は404、`index.html` `muku/index.html` `style.css` は本番と別物。
   古いプライバシーポリシー無しのサイトが公開URLで読める状態なので、放置しない。
   Workers移行は保留と決めた以上、**消すのが筋**。渡部に確認してから
   （消す: `npx wrangler delete --name mssbworks-site`）
2. **`README.md` を直す。**「Netlify で公開」「`netlify.toml`」と書いてあるが、Netlifyは
   2026-06-30にやめている。いまはGitHub Pages。`muku/` `privacy/` も載っていない
3. **`wrangler.jsonc` のコメントを直す。**「引っ越すための設定」「1〜4の手順」と書いてあるが、
   引っ越しは2026-09-05に保留と決まった。読んだ人が手順どおり進めてしまう
4. **`~/mssb/website/CLAUDE.md` を置く。**社内の掟では案件フォルダ直下に置くことになっているが、
   このフォルダには無い
5. GitHub Pagesの Enforce HTTPS が off。`http://mssbworks.com/` が200を返し、httpsへ飛ばない。
   証明書は approved（2026-11-27まで）なので、設定画面でチェックを入れるだけ。
   **渡部がGitHubの設定画面で押す作業**
6. DMARC（`_dmarc`）が無く、DKIM（`google._domainkey`）も引けない。メールの信用に効く。
   別作業として `~/mssb/_company/メールの信用_DMARCとDKIM_20260906.md` を見て進める

## 記録と実物が食い違っていた点（2026-09-15に突き合わせた）

- 記録（README）は「Netlifyで公開」。**実物はGitHub Pages。**Netlifyは2026-06-30に外している
- 記録（`wrangler.jsonc`）は「Workersへ引っ越す準備。1〜4の手順で進める」。
  **実際は2026-09-05に保留と決まっている。**手順3のDNS移行は「中止」
- 記録（2026-06-29の渡部の指示）は「GitHubのPrivateリポジトリで」。
  **実物は public。**GitHub Pagesを無料で使うために変えたと思われるが、そう決めた記録は見つからない。
  未確認
- セッション「mssbworks corporate site」の記録は2026-07-03で終わっているが、
  **2026-08-21のメタタグ追加以降、9月の作業（ムクのページ・Workers準備・窓口・
  プライバシーポリシー）はそのセッションの外で行われている。**
  どのセッションから入ったかは特定できなかった

## 再開手順

1. このファイルを読む
2. `~/mssb/_company/dns_cloudflare移行_20260904.md` を読む（DNS・フォーム・移行の判断の正本）
3. Cloudflareを触るなら `~/mssb/_claude/skills/cloudflare/SKILL.md` を先に読む
4. 手元と本番がずれていないか確かめる

```bash
cd ~/mssb/website
git log --oneline -5
git status --short
python3 .cloudflare/検収.py https://mssbworks.com
```
