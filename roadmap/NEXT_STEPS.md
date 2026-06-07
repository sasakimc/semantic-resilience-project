# 次の一手 / 作業メモ

_最終更新: 2026-06-07（PR #6 マージ済み）_

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

## PR の状況

- **PR #1〜#6: すべて `main` にマージ済み。**
  - PR #6 は査読の指摘5点（paraphrases 実行 / APIキーのリダクション /
    schema の `conversation` 必須化 / `prompt_set_sha256`＋`case_metadata` /
    roadmap の public project log 化）を反映してからマージした。
- 作業ブランチ `claude/charming-cerf-3qhsN` と `main` は内容一致。
- 次に作業する時もこのブランチで作業し、PR を作ってレビュー → マージ、の流れ。

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

## 次回はここから（おすすめ順）

（PR #6 はマージ済み。結果インフラは `main` にある。）

1. **オフライン指標スクリプトを作る**（実データ前でも着手可）:
   `experiments/metrics/compute_metrics.py`。`results/runs/*.jsonl` を読み、
   §5 の black-box 指標を計算する:
   - self_contradiction_rate, paraphrase_consistency,
     prompt_perturbation_sensitivity（paraphrase/repeat のグルーピングが必要）,
     recovery_success_rate, residual_distance_to_baseline, semantic_drift。
   - 注意: semantic_drift / residual_distance は埋め込み元が必要。
     埋め込みモデルとアクセス方法を決めるか、まずは judge ベース/語彙的な
     proxy から始めて「proxy である」と明記する。
   - 出力は (model, case, intensity_level) をキーにした整然テーブル（CSV/JSON）。
2. **本物の結果を入れる**（どちらか選ぶ）:
   - (a) 手元で APIキー付きランナーを実行し `results/runs/*.jsonl` をコミット、または
   - (b) GitHub Actions ワークフロー＋ secrets
     （`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`）で CI 実行。
   - まずは **contradiction ladder** から。崩壊閾値が一番きれいに見える
     （段 0→4 の非線形劣化、段5で P3 の再編成）。
3. **最初の結果まとめ:** 短い `papers/position-paper/RESULTS.md`（または DRAFT に
   §Results を追加）。ラダーの結果を provenance 完備で報告する。
   これが Position Paper を arXiv 向けの「研究論文」に格上げする。

## 小さめの宿題（あると良い）

- `§11 Research Perspective`: プレースホルダを、3〜4文の一人称
  epistemic-provenance 文に置換（構造工学 → 確率/リスク → 複雑系 →
  脳科学 → LLM）。
- contradiction ラダーのワークフローが通ったら、他のストレッサー
  （ambiguity, value-conflict）も段階ラダー化する。
- 公開研究プロジェクトとして LICENSE と CITATION.cff を追加。
- Position Paper の残り章（§0,1,2,7,8,9,10,12）を埋める。
- GitHub の About 文・topics（ai-safety, interpretability,
  cognitive-science）。これは GitHub 設定の手動操作。

## 次回まず答える1問

本物の結果をどう作るか — ローカル実行（3a）か CI＋secrets（3b）か。
この選択で、次のコーディングが「ワークフロー作成」か「指標スクリプトのみ」かが
決まる。
