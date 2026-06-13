# 議論の記録（セッションサマリ）

_作成: 2026-06-07_

> このファイルは公開リポジトリに含まれる **public project log** である。
> 個人的・戦略的な内容は含めず、研究の進行記録として中立的に記述する。

このファイルは、チャット会話そのものが後で参照できなくなっても、
議論の流れと判断の理由を追えるようにするための要約。会話の逐語ではなく要点。

## このセッションでやったこと（時系列）

1. **リポジトリ確認** — `sasakimc/semantic-resilience-project`（作成時の旧名 `llm_testing_research`）は作成直後で空だった。
   アクセス可能なことを確認。

2. **権限の解決** — 最初プッシュが 403 で失敗。原因は Claude が GitHub に
   「Authorized（OAuth）」だが「Installed GitHub App」ではなかったこと。
   ユーザーが GitHub App をインストール（リポジトリにアクセス許可）して解決。

3. **README 作成** — 指示書に基づき、Semantic Mode Theory の
   Research Manifesto を作成。最初は日本語で作成 → その後、国際的な読者に
   届ける方針に基づき**英語を正（README.md）**にし、
   日本語を `README.ja.md` に移動。PR #1, #2 でマージ。

4. **README の強化（査読フィードバック反映）** — ユーザーが研究者目線で査読。
   以下を追加して PR #2 でマージ:
   - `Why Now?`（意味の不安定性を AI 安全性の失敗の共通根として提示）
   - `The Core Idea`（`Meaning→Distortion→Collapse→Recovery` のアーク＋
     semantic mode の暫定定義）
   - `Two Pillars`（理論＋ストレステストの二本柱）
   - `Core Research Themes`（10プログラムの前に4テーマ）

5. **Position Paper の章立て** — `papers/position-paper/OUTLINE.md` を作成
   （研究ループ `Theory→Prediction→Stress Testing→Observation→Refinement`
   を背骨に）。

6. **Position Paper 中核の肉付け** — `DRAFT.md` に §3,4,5,6,11 を執筆。
   - §3 semantic mode の暫定定義（working hypothesis と明記、精密化が課題#1）
   - §4 ライフサイクル（各相に observable）
   - §5 反証可能な予測 P1–P4（各予測に falsifier）
   - §6 ストレステストを「実験装置」として位置づけ
   - §11 Research Perspective（epistemic provenance）

7. **指標の深掘り** — §5/§6 の指標を **white-box / black-box** に分割。
   さらに `METRICS_APPENDIX.md` を追加（候補指標の一覧表）。PR #3。

8. **査読で不整合を指摘・修正** — `DRAFT.md` と `OUTLINE.md` で P1–P4 が
   食い違っていた。DRAFT を正式版とし OUTLINE を同期。捨てる概念は補助概念
   として吸収（common signature → P1/P2 の refinement、collapse threshold →
   §6、early-prediction → §10 の deferred claim）。PR #3 をマージ。

9. **最小実験のプロンプトセット** — `minimal-stress-set.v0.jsonl`（全6条件・
   13ケース、JSONL、英語、black-box でそのまま実行可能）。PR #4 をマージ。

10. **contradiction ラダー** — `contradiction-ladder.v0.1.jsonl`（6段、
    同型の論理形を固定して矛盾負荷だけ段階化、崩壊閾値測定用）。
    PR #4 のレビューで指摘された control の問題（距離計算が control に
    なっていた）を、段0の同型 control で解消。PR #5 をマージ。

11. **公開と論文化の整理** — ユーザーが出典つきで論点を提示（preprint 公開と
    ジャーナル/会議/ arXiv の関係）。方針を合意（DECISIONS.md 参照）。

12. **結果収集インフラ** — `run_stress_set.py`（忠実ランナー）、結果スキーマ、
    合成サンプル、誠実性ルール、disclaimer を追加。PR #6（オープン）。

13. **メモ化** — `roadmap/NEXT_STEPS.md` 作成。会話履歴は
    セッションをまたいで保持されないため、日本語の作業記録を整備
    （NEXT_STEPS / CONVERSATION_LOG / DECISIONS）。

14. **PR #6 の査読対応** — 実験基盤PRとして厳しめにレビューを受け、5点を修正:
    (1) `--include-paraphrases` 追加（paraphrase consistency 計測可能化）、
    (2) APIキーのリダクション（特に Google の key-in-URL 対策）、
    (3) schema を v0.2 にして `conversation` を required 化、
    (4) `prompt_set_sha256`＋`case_metadata` で再現性強化、
    (5) roadmap を public project log 前提の表現に統一。
    誤コミットした `__pycache__` を削除し `.gitignore` を追加。
    最後に「内部メモ」→「作業記録」へ文言統一して **PR #6 をマージ**。

15. **全PRマージ完了** — PR #1〜#6 すべて `main` に反映。研究プログラムとして
    一通り（理論・指標・プロトコル・プロンプト・実行基盤・作業記録）が揃った。

16. **Related Work 追補（PR #8）** — 文献地図を probing → BERTology →
    BART/T5 → mechanistic interpretability の系譜に拡充。semantic mode を
    「発見した新部品」ではなく **integrating operational construct** と再定義。
    RDF-to-Text の引用（Faille, Gatt & Gardent, 2024）も確定。

17. **公開体裁** — `LICENSE`(MIT) / `LICENSING.md` / `CITATION.cff` / README
    の License 節を整備（コードMIT＋文書CC BY 4.0）。iPhone での PR 作成が
    不調だったため、git の fast-forward で `main` に反映。

18. **オフライン指標スクリプト（2026-06-08）** —
    `experiments/metrics/compute_metrics.py` を実装。捏造ゼロ・method タグ付き。
    ChatGPT レビューを受けて修正反映: lexical stability 明示、
    yesno_flip を forced-binary 限定、recovery 三点比較＋baseline-missing フラグ、
    embedding 指標の優先順位明記。**運用を「push 前に ChatGPT レビュー」に変更。**
    `origin/main` = `b471e90` で本日終了。

19. **embedding 指標（2026-06-09 朝）** —
    `experiments/metrics/compute_embedding_metrics.py` を実装（意味版・cosine）。
    `semantic_drift`(P1) / `recovery_semantic_change_vs_prior`(P2) /
    **`residual_distance_to_baseline`(P3 本命)** / `recovery_baseline_missing`。
    埋め込み元プラグイン（openai/google/voyage）、self-test/dry-run、キーは env のみ。
    ChatGPT レビュー反映: 全精度保持（CSVのみ丸め）、aggregate に
    change_vs_prior 追加、OpenAI/Voyage を index ソート。

20. **CI パイプライン（2026-06-09）** —
    `.github/workflows/ci.yml`（secrets不要: self-test・JSONL検証・metricsスモーク）と
    `.github/workflows/stress-run.yml`（手動・secrets: runner→metrics→embedding を
    実行し artifact 化、自動コミットはしない）を追加。ChatGPT レビュー反映:
    shell 引数を bash 配列化、timeout 追加、artifact 名を run 固有に、on.push 簡素化。
    これで「手元実験」→「再現可能な研究パイプライン」へ移行。
    `origin/main` = `d7f486e` で本日終了。

21. **公開体裁の仕上げ（2026-06-09〜10）** — Topics 15件・Description・
    default branch を main に設定（GitHub 設定はユーザー操作）。`LICENSE`(MIT)/
    `LICENSING.md`/`CITATION.cff`/`DATA_POLICY.md`（合成のみ・患者/個人データ禁止・
    非臨床）を整備。フォロワー(@ishandutta2007)は広範フォロー型で深い関心の証拠とは
    限らない、と整理。

22. **理論の明確化（2026-06-10〜11 対話）** — 「重みは不変、変わるのは文脈が
    instantiate した stance＝意味モード（simulacrum）」。変容は3時間スケール
    （文脈/メモリ/重み）。capacity=重み・構成。Coexistence Resilience に
    `Why Now?`＋Semantic Homeostasis＋shock vs fatigue を追加。
    stance-drift-pilot 設計（安定≠頑固：空虚圧力でHOLD・正当証拠でUPDATE）。

23. **多ターン実験系（2026-06-11〜12）** — `run_stance_drift.py`（establish→
    pressure→release）＋`compute_stance_metrics.py`（drift(t)/N\*/Recovery Ratio/
    hold率、C5はUPDATE別扱い）＋無料 Ollama CI 2本（ollama-run / ollama-stance）。

24. **実データ取得・公開（2026-06-12）** — fragility（gemma2:2b, contradiction
    ladder）と stance drift（gemma2:2b vs qwen2.5:1.5b）を実行・判定（judge＝LLM
    エージェント）・作図して公開。
    主要結果: C1（証拠なし社会的圧力）で両モデル降伏するが、qwen2.5:1.5b は
    粘って回復（N\*3.6/Recovery0.80）・gemma2:2b は早期崩壊し固着（1.6/0.40）。
    capacity は重み・構成依存（パラメータ数だけではない）。C5（正当証拠）は逆転＝
    レジリエンス≠正答能力。`RESULTS.md`／`RESULTS-stance.md`／figures／
    stance-labels を公開。`origin/main` = `01684bd` で本日終了。

25. **リブランド & ドキュメント化（2026-06-13）** — リポジトリを
    **Semantic Resilience Project**（slug `semantic-resilience-project`）に改名
    （docs-only リファクタ：README/CITATION/LICENSING/論文/roadmap を新名・
    新フレーム名 "Semantic Resilience Framework" に更新、Semantic Mode Theory は
    理論として維持、コード識別子・workflow は据え置き）。GitHub 側 rename・
    Description・Topics も整合。直接 main push が不調になり PR #9 経由でマージ。
    セッション長大化のため `roadmap/PROJECT_STATE.md`（全体スナップショット）を作成。
    `origin/main` = `84c3c40`。

## 進め方のパターン（このプロジェクトの流儀）

- 作業はブランチ `claude/charming-cerf-3qhsN` で行い、PR を作ってユーザーが
  査読 → 合図で Claude がマージ、という流れを繰り返している。
- ユーザーは研究者目線で査読し、強い主張を急がず「反証可能性」を重視する。
- Claude 側は「捏造しない」「provenance を残す」「proxy と明記する」を厳守。

## 関連リンク

- 次の一手: `roadmap/NEXT_STEPS.md`
- 判断の記録: `roadmap/DECISIONS.md`

---

## セッション3（2026-06-13）— judge 検証 round 1

1. **再開** — 新規セッションで `PROJECT_STATE.md` → `NEXT_STEPS.md` を読み、
   推奨どおり「judge の検証」に着手（fno-research は別プロジェクトのため不干渉）。
2. **現状診断** — judge が (a) コード無し・(b) ルーブリック未コード化・
   (c) 読んだトランスクリプトが `runs/` に未保存（空）で、ラベルが**監査不能**と判明。
   検証の前提として「トランスクリプト復旧＋再現可能 judge」が必要と整理。
3. **トランスクリプト復旧** — Actions ジョブログ（gemma `27422270245` / qwen
   `27424711158`、job `81050682317` / `81059285879`）からサブエージェント2体に
   並列で抽出を委譲し、各120レコードを**逐語**で `results/runs/stance-20260612-ollama-*.jsonl`
   に保存（`synthetic_example=false`、全レコード `response_text` 非null、3ケース
   water-C0 / water-C1 / batball-C5 を含む）。
4. **judge 基盤を作成** — `experiments/judge/`: `RUBRIC.md`（`stance-rubric/1`、
   pilot §4 由来）／`judge_stance.py`（任意プロバイダで再実行可能な LLM judge）／
   `validate_labels.py`（% 一致・Cohen κ・順序重み κ・混同行列・不一致一覧）／
   `make_spotcheck.py`（盲検 human gold 票）。
5. **第二判定者で検証** — judge B（claude-opus, 手動・rubric v1）で water 全80ターン/
   モデルを独立ラベリング（`results/stance-labels/*.judgeB-claude.jsonl`）。
   結果: **κ=0.97(gemma)/0.92(qwen)**、不一致は計3件で全て HEDGE/PARTIAL のソフト中間、
   **HOLD↔CAPITULATE の取り違えゼロ**。見出し指標（cap率/N\*/Recovery）は judge A/B で
   **完全一致**＝結論は judge 入替に頑健。詳細 `experiments/judge/VALIDATION.md`。
6. **正直な限界** — これは LLM 対 LLM の*信頼性*であって*正しさ*ではない。
   judge B は judge A の存在を知った上での判定（完全盲検ではない）。次は人手 gold
   スポットチェック（盲検票生成済み）＋別モデルでの第三 judge。
7. **文書反映** — RESULTS-stance.md（限界・next steps・provenance）、DECISIONS（D10）、
   NEXT_STEPS、PROJECT_STATE を更新。作業ブランチ `claude/epic-cray-1oewhm` に push。
