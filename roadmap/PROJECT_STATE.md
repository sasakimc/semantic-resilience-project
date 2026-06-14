# プロジェクト現況スナップショット（PROJECT STATE）

_作成: 2026-06-13。新規セッションは **この1枚** → `NEXT_STEPS.md` の順に読めば全体を把握して再開できる。
役割分担: PROJECT_STATE=全体地図 / NEXT_STEPS=次の一手 / DECISIONS=判断と理由 / CONVERSATION_LOG=履歴。_

## 1. アイデンティティ
- **Repository**: `sasakimc/semantic-resilience-project`（旧 `llm_testing_research`、GitHub 自動リダイレクト）
  - URL: https://github.com/sasakimc/semantic-resilience-project ／ default branch `main` ／ public
- **Project name**: Semantic Resilience Project
- **Core theory**: Semantic Mode Theory（理論）／ **Empirical framework**: Semantic Resilience Framework（実証＝ストレステスト手法）
- **License**: code=MIT / docs=CC-BY-4.0（`LICENSING.md`）。**Data policy**: 合成のみ・実個人/患者データ禁止・非臨床（`DATA_POLICY.md`）。
- 開発ブランチ: `claude/charming-cerf-3qhsN` → `main` に FF（直接 push 不調時は **PR 経由マージ**）。

## 2. 一言サマリ
脳・認知・LLM に共通する **意味の「形成→歪み→崩壊→回復」** を、**構造信頼性工学のように測る**研究プログラム。
- **shock（単発の矛盾）= fragility**、**fatigue（累積／長期相互作用）= coexistence / stance drift**。
- 核心仮説: **回復＝復元(restoration)ではなく再編成(reorganization)**。
- 中間概念: **stance＝文脈が instantiate した意味モード（"エンティティ"／simulacrum）**。重みは不変、変わるのは文脈状態（3時間スケール: 文脈 / メモリ / 重み）。**capacity＝重み・構成**。

## 3. リポジトリ構成（各ファイルの役割）
```
README.md / README.ja.md      マニフェスト（英語が正）
DATA_POLICY.md                合成のみ・患者/個人データ禁止・非臨床
LICENSE / LICENSING.md / CITATION.cff
papers/position-paper/
  OUTLINE.md                  全体章立て
  DRAFT.md                    中核章（§2 Related Work, §3 仮説, §4 lifecycle,
                              §5 予測P1–P4, §6 Semantic Resilience Framework, §11 provenance）
  METRICS_APPENDIX.md         候補指標（black-box/white-box）
  SEMANTIC_FRAGILITY.md       fragility 曲線・limit state・aleatory/epistemic
  RESULTS.md                  初回結果: fragility（gemma2:2b）＋図
  RESULTS-stance.md           初回結果: stance drift（gemma2 vs qwen）＋図
  figures/                    *.png（結果図）
experiments/
  prompts/                    minimal-stress-set.v0 / contradiction-ladder.v0.1 / stance-pressure.v0
  runners/                    run_stress_set.py（単発）/ run_stance_drift.py（多ターン）
  metrics/                    compute_metrics.py（lexical）/ compute_embedding_metrics.py（cosine）/
                              compute_stance_metrics.py（drift/N*/Recovery Ratio）
  results/
    schema/ templates/ runs/(stance トランスクリプト復旧済) stance-labels/(judge A/B出力＋一致＋盲検票)  README
  judge/                      RUBRIC(stance-rubric/1) / judge_stance.py(再現judge) /
                              validate_labels.py(κ) / make_spotcheck.py(盲検票) / VALIDATION.md(検証報告)
  coexistence/stance-drift-pilot.md   本丸の実験設計
notes/research-ideas/coexistence-resilience.md  共生レジリエンス（fatigue/homeostasis）
.github/workflows/            ci.yml / stress-run.yml / ollama-run.yml / ollama-stance.yml
roadmap/                      PROJECT_STATE(これ) / NEXT_STEPS / DECISIONS / CONVERSATION_LOG /
                              OVERVIEW(.md/.ja: 考え方の地図＝Heidegger/Alexander/Umwelt の枠) / reviews/(外部レビュー)
```
**注意（挙動不変のため据え置き）**: `run_stress_set.py` / `stress-run.yml` / `stress-pressure.v0.jsonl` /
スキーマ文字列 `stance-drift/0.1` 等の "stress" を含む識別子・ファイル名は改名していない。

## 4. 理論の骨子
- **P1** ストレスで意味構造が測定可能に変化 / **P2** ハルシネーション＝モード不安定性と相関 /
  **P3** 回復は再編成（baseline に戻らない）/ **P4** 認知歪みプロンプトは類似の偏りを誘発。各予測に **falsifier**。
- **二種の壊れ方**: shock=fragility 曲線 `P(collapse|stress)`、fatigue=累積（S–N 的）。
- **limit state**（崩壊判定）を先に定義しないと fragility は無意味。
- **stability ≠ rigidity**: 空虚な圧力では HOLD、正当な証拠では UPDATE。

## 5. 実験系の回し方（運用フロー）
1. **GitHub Actions**（無料・キー不要・スマホ可）: `Ollama run`（fragility）/ `Ollama stance-drift`（多ターン）を
   **Run workflow** で起動（model だけ選ぶ: gemma2:2b / qwen2.5:1.5b 等）。
2. 結果は **ジョブログに出力**される（artifact もあるが、その保存先 Azure blob は本環境の
   許可リスト外で**直ダウンロード不可** → だからログ出力にしてある）。
3. ログは MCP `get_job_logs` で取得 → **巨大なのでサブエージェントに解析＋ judge を委譲**（定石）。
4. `experiments/metrics/compute_*_metrics.py` で集計・作図。
- 指標は3層: **lexical**(stdlib) / **embedding**(cosine) / **judge**(LLM, round 1 検証済
  κ0.92–0.97・`experiments/judge/`)。lexical heuristic は judge と κ≈0.07 で proxy 不適。

## 6. これまでの結果（実データ・パイロット）
- **Fragility（gemma2:2b, contradiction ladder, n=10）** → `RESULTS.md`:
  最終回答(yes/no)は前提に素直に追従するが、**崩壊は推論に出る**（不可能段 L4 で半数しか矛盾を認識せず muddled）。
  回復は再編成的。
- **Stance drift（gemma2:2b vs qwen2.5:1.5b, C1=証拠なし社会的圧力, n=5）** → `RESULTS-stance.md`:
  両モデルとも降伏（rate 1.0）だが、**qwen2.5:1.5b は粘って回復**（N\*=3.6 / Recovery=0.80 / 固着 1/5）、
  **gemma2:2b は早期崩壊し固着**（N\*=1.6 / Recovery=0.40 / 固着 3/5）。
  → **capacity は重み・構成依存（パラメータ数だけではない）**。C5（正当証拠）は逆転 → **レジリエンス≠正答能力**。

## 7. 運用の流儀（重要・必読）
- **push 前に ChatGPT レビュー**：ローカル commit（push しない）→ `git diff origin/main..HEAD` を
  ファイルで渡す → OK で push → main を FF。
- **直接 main push が不調**になることがある（特にリネーム後）→ **MCP の PR 作成＋マージ**で代替（旧名
  `llm_testing_research` 指定でも GitHub がリダイレクトして成功する）。リモート/MCP は旧名スコープだが
  リダイレクトで現状機能。
- **捏造ゼロ**：実行は人間/CI、結果は provenance 付き、合成データのみ。
- コミットは未署名（committer `noreply@anthropic.com`）で GitHub 上 "Unverified" 表示になるが**既知・無害**。
  Stop フックは GitHub マージコミット（`noreply@github.com`）を除外済み。

## 8. 既知の弱点 / open questions
- ~~**judge が LLM エージェント1回・未検証**（いまの最大の弱点）。~~ → **round 1 検証済み
  （2026-06-13）**：第二判定者と κ=0.97/0.92、見出し指標は judge 入替で不変。ただし
  LLM 対 LLM の信頼性であって正しさではない → **人手 gold 検証が次の弱点**
  （盲検票生成済み）。`experiments/judge/VALIDATION.md` 参照。
- **N=1 系・項目少数・n=5** のパイロット。確定的主張ではない。
- **Recovery Ratio が"意味的回復"を表すか**の妥当性検証が必要。
- **Semantic Homeostasis の正式定義**（保持＋適応＋回復の統合指標）。
- **脳ネットワークとの対応**（sticky drift＝意味固着の*類推*、ただし非臨床）。

## 9. 次の一手（`NEXT_STEPS.md` と同期）
1. ~~**judge の検証**~~ ✅ round 1 済（κ 0.92–0.97、`experiments/judge/`）→ 次は
   **人手 gold スポットチェック**（`results/stance-labels/spotcheck-*.BLANK.jsonl` を埋める）＋別モデル第三 judge。
2. **ストレッサー拡張**（authority / flattery / emotional / isolation）＝共生ストレス。
3. **Stability Scorecard 化**（合格条件＝空虚圧力で HOLD・正当証拠で UPDATE・解放後 recover）。
4. embedding ベースの stance 距離 / 長期 fatigue。

## 10. セッション運用メモ
- 旧スナップショット時点 `origin/main` = `84c3c40`。
- **session-3（2026-06-13）**: judge 検証 round 1 を実施。作業ブランチ
  `claude/epic-cray-1oewhm`（main の先端 `08613d8` から派生）。judge 基盤＋
  トランスクリプト復旧＋検証結果を push 済み。`main` への反映は従来どおり FF/PR で。
- このセッション（session_01X432…）は長大化したため、**次は新規セッション推奨**。
  冒頭で `roadmap/PROJECT_STATE.md` → `roadmap/NEXT_STEPS.md` を読むこと。
