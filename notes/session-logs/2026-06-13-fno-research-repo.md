# Session memo — 2026-06-13: new repository plan (`fno-research`)

> セッションが長くなったので、ここまでの経緯と結論をメモとして残す。
> Branch: `claude/new-input-repository-h2a4nu`

## 背景 / きっかけ

- 「あたらしいリポジトリを作りたい」という相談から始まった。
- 当初は語が曖昧だったため確認 → **新しいGitHubリポジトリ**を作りたい、という意図と判明。

## 議論で決めたこと

1. **既存リポジトリとのバッティング懸念について**
   - GitHubのリポジトリは各々独立。**新しい名前**で作る限り `semantic-resilience-project` には一切影響しない。
   - 名前の衝突が起きるのは「まったく同じ名前」で作ろうとした時だけ(その場合もGitHubがエラーで弾くので上書きの心配はない)。
   - 現状 `sasakimc` アカウントの公開リポジトリは `semantic-resilience-project` の1つのみ。

2. **方針: リポジトリ単位で育てる**
   - 「リポジトリ単位で育てていきたい」という意向から、既存プロジェクト内のフォルダ追加ではなく、**別リポジトリを新規作成**する方針に決定。

3. **作りたいリポジトリ**
   - 名前: **`fno-research`**
   - テーマ: **Neural Operator(FNO / Fourier Neural Operator)に関する研究**
   - これは `semantic-resilience-project` とは**全く別物**のプロジェクト。
   - 希望設定: Private / README付き。

## 結果 / ブロッカー

- セッションからの自動作成を試みたが、**403 "Resource not accessible by integration"** で失敗。
- 原因: 本セッションのGitHub連携は **`sasakimc/semantic-resilience-project` の1リポジトリのみ**にスコープが絞られており、**リポジトリ作成権限が無い**。

## 次のアクション (TODO)

- [ ] **ユーザー本人が `fno-research` を作成**(後で対応する、と合意済み)
  - https://github.com/new → name: `fno-research` / Private / Add README
- [ ] 作成後、このセッション(または新セッション)で中身を育てたい場合:
  - `list_repos` で利用可能リポジトリを確認 → セッションに `fno-research` を追加
  - その後 README整備・ディレクトリ構成・PyTorch等の雛形コードを準備可能

## メモ

- `fno-research` の中身は未着手。リポジトリ作成はユーザー側で実施予定。
- 本メモは経緯の記録用であり、`semantic-resilience-project` の研究内容そのものとは独立。
