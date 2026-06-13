# 次の一手 / 作業メモ

_最終更新: 2026-06-12（実データ取得：fragility＋stance drift＋モデル比較を公開。`origin/main` = `01684bd`）_

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

- **リポジトリ名は Semantic Resilience Project に改名済み**（slug `semantic-resilience-project`、
  2026-06-13）。中核理論＝**Semantic Mode Theory**（内部維持）、実証フレーム＝
  **Semantic Resilience Framework**。新URL: https://github.com/sasakimc/semantic-resilience-project
  （旧 `llm_testing_research` は自動リダイレクト）。コード識別子・ファイル名・
  workflow `name:` は据え置き（挙動不変）。
- README は英語が正（国際公開向け）。日本語は `README.ja.md` にミラー。
- `roadmap/` 配下の作業記録は日本語で統一。
- 二本柱: **Semantic Mode Theory**（説明）＋ **Semantic Resilience Framework**（実証）。
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

## ✅ 済んだこと（2026-06-12）— 実データを取得・公開

- **無料 Ollama CI** を追加：`.github/workflows/ollama-run.yml`（fragility）＋
  `.github/workflows/ollama-stance.yml`（多ターン stance drift）。スマホから実行可・
  結果をログに出力（私が読み取り）・artifact 化（自動コミットなし）。
- **多ターン基盤**：`run_stance_drift.py`（establish→pressure→release）＋
  `compute_stance_metrics.py`（drift(t)/N\*/Recovery Ratio/hold率、C5は UPDATE 別扱い）。
- **初回結果（公開済み）**:
  - `papers/position-paper/RESULTS.md` — fragility 単発（gemma2:2b）。崩壊は最終回答でなく
    推論に出る／回復は再編成。
  - `papers/position-paper/RESULTS-stance.md` — **本丸**：C1（証拠なし社会的圧力）で
    両モデル降伏するが、**qwen2.5:1.5b は粘って回復(N\*3.6/Recovery0.80)・gemma2:2b は
    早期崩壊し固着(1.6/0.40)**。capacity は重み・構成依存（パラメータ数だけではない）。
    C5（正当証拠）は逆転：gemma 健全・qwen 乱れ＝レジリエンス≠正答能力。
  - judge ラベルは `experiments/results/stance-labels/` に保存（judge＝LLMエージェント1回・未検証）。

## 次回はここから（研究本番：コードより設計・検証が勝負）

1. **judge の検証**：人手スポットチェック／複数 judge で stance ラベルの信頼性を確認。
   （現在は LLM エージェント1回・未検証。ここが今の最大の弱点。）
2. **ストレッサー拡張**：C1 以外に authority / flattery / emotional / isolation /
   反復否定 を `stance-pressure` に追加 → 本格的な「共生ストレス」バッテリーへ。
3. **項目数・反復・モデルを増やす**：stance 1項目→複数、n=5→大きく、他モデル（gpt-oss等）。
4. **Stability Scorecard 化**：合格条件＝「空虚な圧力で HOLD・正当証拠で UPDATE・解放後 recover」。
   CI 回帰ゲートに。
5. （任意）**長期 fatigue**（多数ターンの累積）と **embedding ベースの stance 距離**。

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
  cognitive-science）。✅ 設定済み（default branch も main 済み）。

## 実データの取り方（確立済み・スマホ完結）

GitHub **Actions → 「Ollama stance-drift」or「Ollama run」→ Run**（model だけ選ぶ：
`gemma2:2b` / `qwen2.5:1.5b` 等、temperature/repeats は既定）。完了後、結果は
**ジョブログに出力**される（artifact もある）。ログは MCP `get_job_logs` で読めるが
巨大なので、**サブエージェントに解析＋ judge を任せる**のが定石。ダウンロード先の
Azure blob は本環境の許可リスト外で直取得不可（だからログ出力にしてある）。

## ☀️ 次回の再スタート用

1. この `NEXT_STEPS.md` を開く（いまここ）。
2. 「次回はここから」の **1. judge の検証**から進めるのがおすすめ
   （結果の信頼性がいまの最大の弱点）。
3. もしくは **2. ストレッサー拡張**（authority/flattery/emotional/isolation）。
- 中断時の状態: `origin/main` = `01684bd`、全変更マージ済み、未push の保留なし。
