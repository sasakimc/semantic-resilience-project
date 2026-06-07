# 議論の記録（セッションサマリ）

_作成: 2026-06-07_

> このファイルは公開リポジトリに含まれる **public project log** である。
> 個人的・戦略的な内容は含めず、研究の進行記録として中立的に記述する。

このファイルは、チャット会話そのものが後で参照できなくなっても、
議論の流れと判断の理由を追えるようにするための要約。会話の逐語ではなく要点。

## このセッションでやったこと（時系列）

1. **リポジトリ確認** — `sasakimc/llm_testing_research` は作成直後で空だった。
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

13. **本日終了・メモ化** — `roadmap/NEXT_STEPS.md` 作成。会話履歴は
    セッションをまたいで保持されないため、日本語の作業記録を整備。

## 進め方のパターン（このプロジェクトの流儀）

- 作業はブランチ `claude/charming-cerf-3qhsN` で行い、PR を作ってユーザーが
  査読 → 合図で Claude がマージ、という流れを繰り返している。
- ユーザーは研究者目線で査読し、強い主張を急がず「反証可能性」を重視する。
- Claude 側は「捏造しない」「provenance を残す」「proxy と明記する」を厳守。

## 関連リンク

- 次の一手: `roadmap/NEXT_STEPS.md`
- 判断の記録: `roadmap/DECISIONS.md`
