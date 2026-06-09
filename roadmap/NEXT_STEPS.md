# 次の一手 / 作業メモ

_最終更新: 2026-06-09（embedding 指標 + CI パイプライン まで完了。`origin/main` = `d7f486e`）_

再開を速くするための引き継ぎメモ。次回はまずこのファイルを開くこと。

## 現在地

空のリポジトリから、理論・測定設計・プロンプトセット・（今回）結果収集インフラまで揃った
「研究プログラム」になった。これまでの流れ:

```text
README（マニフェスト）
  → Position Paper 中核（§3,4,5,6,11）
    → Metrics Appendix（候補指標）
      → Minimal Protocol（最小実験設計）
        → Prompt Set v0（全6条件）
          → Contradiction Ladder v0.1（崩壊閾値ラダー）
            → 結果スキーマ＋忠実ランナー（PR #6・オープン）
```

## リポジトリ構成（現在）

```text
README.md / README.ja.md                  マニフェスト（英語が正・日本語ミラー）
papers/position-paper/
  OUTLINE.md                              全体の章立て地図
  DRAFT.md                                中核の章、正式版 P1–P4
  METRICS_APPENDIX.md                     black-box / white-box 候補指標
experiments/
  minimal-protocol.md                     最初の最小実験設計
  prompts/
    minimal-stress-set.v0.jsonl           全6条件・13ケース
    contradiction-ladder.v0.1.jsonl       6段（neutral→impossible→recovery）
    README.md                             プロンプトセットのスキーマ
  runners/
    run_stress_set.py                     APIランナー（anthropic/openai/google）, --dry-run対応
    README.md
  results/
    schema/run-record.schema.json         provenance完備の記録スキーマ
    templates/...SCHEMA-EXAMPLE.jsonl      合成サンプル（実データではない）
    runs/                                  本物の実行結果はここに入れる（現在は空）
    README.md                             誠実性ルール
roadmap/
  NEXT_STEPS.md                           このファイル
  CONVERSATION_LOG.md                     今日の議論の記録
  DECISIONS.md                            重要な判断の記録
```

## PR の状況 / 直近の作業

- **PR #1〜#8: すべて `main` にマージ済み。** その後の小さな変更（LICENSE/
  CITATION、オフライン指標スクリプト、レビュー反映）は、作業ブランチに commit →
  `main` に **fast-forward して push** する形で反映済み。
- `origin/main` 先端 = `b471e90`（2026-06-08 終了時点）。
- 作業ブランチ `claude/charming-cerf-3qhsN` と `main` は内容一致。
- **運用変更（重要）**: これ以降は **push の前に ChatGPT レビューを通す**。
  手順 = ローカル commit（push しない）→ `git diff origin/main..HEAD` を
  ファイルで渡して ChatGPT レビュー → OK なら push → main を FF。
- GitHub の PR 作成 UI は iPhone だと「nothing to compare」になりやすい
  （スラッシュ入りブランチ名）。確実なのは git での FF マージ。

## 確定した方針

- README は英語が正（国際公開向け）。日本語は `README.ja.md` にミラー。
- `roadmap/` 配下の作業記録は日本語で統一。
- 二本柱: **Semantic Mode Theory**（説明）＋ **Stress Testing Framework**（実証）。
  ループ `Theory → Prediction → Stress Testing → Metrics → Refinement` で接続。
- 正式な予測体系は `DRAFT.md` §5（P1–P4）。`OUTLINE.md` は常にこれと同期させる。
- 指標は「意味そのものの直接測定」ではなく operational proxies。
- **データ捏造は絶対にしない。** 本物の実行には APIキー/ネットワークが要り、
  人間または secrets 付き CI が行う。アシスタントがモデルになりきって生成しない。
- リポジトリは *preliminary / working hypothesis / not peer-reviewed* と明記済み。

## 公開と論文化の注意（後で効く）

- preprint/GitHub 公開は通常ジャーナル投稿を妨げない（例: Nature Portfolio）。
  ただし最終投稿先の方針は投稿前に必ず確認。
- NeurIPS/ICLR のダブルブラインドでは、実名 GitHub リンクではなく
  **匿名化したコードリポジトリ/ZIP** を投稿に使う。
- arXiv へは「純粋な提案」ではなく **初期実験を含む research article** として出す。

## ✅ 済んだこと（2026-06-08）

- 公開体裁: `LICENSE`(MIT) / `LICENSING.md` / `CITATION.cff` / README の License 節。
- **オフライン指標スクリプト `experiments/metrics/compute_metrics.py` 実装＋ChatGPTレビュー反映済み。**
  - black-box 指標を method タグ付きで算出（structural / lexical / requires_embedding / requires_judge）。捏造ゼロ。
  - lexical 指標は「**lexical stability proxy**（表面形式・意味ではない）」と明示。
  - `yesno_flip_rate` は **forced-binary 限定**（`answer_format:"binary"`）の collapse *proxy*。
  - recovery は三点比較: `recovery_lexical_change_vs_prior` ＋ `recovery_lexical_distance_vs_baseline`（matched_control 参照）＋ `recovery_baseline_missing` フラグ。

## ✅ 済んだこと（2026-06-09）

- **embedding 指標 `experiments/metrics/compute_embedding_metrics.py`**（意味版・cosine）。
  `semantic_drift`(P1) / `recovery_semantic_change_vs_prior`(P2) /
  **`residual_distance_to_baseline`(P3 本命)** / `recovery_baseline_missing`。
  埋め込み元プラグイン（openai/google/voyage）、self-test/dry-run。ChatGPTレビュー反映済み。
- **CI パイプライン**: `.github/workflows/ci.yml`（secrets不要の自動チェック）＋
  `.github/workflows/stress-run.yml`（手動・secrets で runner→metrics→embedding を
  実行し artifact 化、自動コミットなし）。→「再現可能な研究パイプライン」に到達。

## 次回はここから（おすすめ順）

**残るは「本物の結果投入」だけ。** コード基盤（runner / metrics / embedding / CI）は揃った。

1. **本物の結果を入れる**（どちらか選ぶ）:
   - (1a) 手元で APIキー付きランナーを実行 → `experiments/results/runs/*.jsonl` をコミット。
   - (1b) リポジトリに secrets 登録（`ANTHROPIC_API_KEY` 等）→ Actions タブの
     **「Stress run」** を手動実行 → artifact をダウンロード → 確認してコミット。
   - まずは **contradiction ladder** から（段 0→4 の非線形劣化、段5で P3 の再編成）。
2. **集計**: 取得後に
   `python experiments/metrics/compute_metrics.py --runs experiments/results/runs/*.jsonl --out-prefix ...`
   ＋（埋め込み元を決めて）`compute_embedding_metrics.py` を実行。
3. **最初の結果まとめ:** 短い `papers/position-paper/RESULTS.md`（または DRAFT に
   §Results）。provenance 完備で報告 → arXiv 向け research article に格上げ。
   ※ データ前でも RESULTS.md の枠（章立て・記入欄）は先に作れる。

## 小さめの宿題（あると良い）

- ~~公開研究プロジェクトとして LICENSE と CITATION.cff を追加。~~ ✅ 済
- `§11 Research Perspective`: プレースホルダを、3〜4文の一人称
  epistemic-provenance 文に置換（構造工学 → 確率/リスク → 複雑系 →
  脳科学 → LLM）。
- Position Paper の残り章（§0,1,7,8,9,10,12）を埋める（§2 Related Work は済）。
- contradiction ラダーのワークフローが通ったら、他のストレッサー
  （ambiguity, value-conflict）も段階ラダー化する。
- embedding 指標の発展（README 記載）: Google batchEmbedContents /
  baseline を分布として扱う / cosine を超える距離（Mahalanobis・近傍シフト）。
- GitHub の About 文・topics（ai-safety, interpretability,
  cognitive-science）。これは GitHub 設定の手動操作（あなた側）。

## 次回まず答える1問

本物の結果をどう作るか — ローカル実行（1a）か CI＋secrets（1b）か。
（CI ワークフローは既に用意済みなので、1b は secrets 登録 → 実行ボタンだけ。）

## ☀️ 次回の再スタート用

1. この `NEXT_STEPS.md` を開く（いまここ）。
2. 「次回まず答える1問」（1a ローカル / 1b CI）を決める。
3. データ取得 → 集計（lexical＋embedding）→ `RESULTS.md` へ。
4. APIキーがまだ用意できないなら、コードだけで進む **RESULTS.md の枠作り**を先に。
- 中断時の状態: `origin/main` = `d7f486e`、全変更マージ済み、未push の保留なし。
