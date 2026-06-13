# 判断の記録（Decision Log）

_作成: 2026-06-07_

> このファイルは公開リポジトリに含まれる **public project log** である。
> 研究上の設計判断とその理由のみを記述し、個人的・戦略的な内容は含めない。

重要な設計・運用上の判断と、その理由を残す。後から「なぜそうしたか」を
追えるようにするためのもの。新しい判断は下に追記していく。

---

## D1. README は英語を正にする

- **判断:** `README.md` を英語（国際公開向け）、`README.ja.md` を日本語ミラーにする。
- **理由:** AI 安全性・解釈可能性・脳/認知科学の国際的な研究コミュニティや
  preprint 読者に届けるため。
- **補足:** `roadmap/` 配下の作業記録は日本語で統一（作業の思考用）。

## D2. 二本柱で構成する

- **判断:** Semantic Mode Theory（説明）と Semantic Resilience Framework（実証）の
  二本柱にする。
- **理由:** 理論だけだと「面白いが検証可能か？」、ストレステストだけだと
  「新しいベンチか？」で終わる。両者を `Theory→Prediction→Stress Testing→
  Observation→Refinement` のループでつなぐと研究プログラムになる。

## D3. 強い主張を急がない／反証可能性を最優先

- **判断:** `propose / hypothesize / may be understood` を使い、`proven` は
  使わない。各予測 P1–P4 に必ず falsifier（反証条件）を添える。
- **理由:** 哲学的エッセイではなく科学的研究プログラムとして読まれるため。

## D4. semantic mode は「暫定定義」として置く

- **判断:** 「ネットワーク内の意味的振る舞いを組織化する、支配的な低次元
  表現構造」と暫定定義し、精密化（測定基準＋behavioral signature）を
  研究課題#1 とする。
- **理由:** 研究者は必ず「semantic mode とは何か」を問う。未定義のまま
  放置せず、しかし断定もしない態度を取る。

## D5. 正式な予測体系は DRAFT.md に置く

- **判断:** P1–P4 の正式版は `DRAFT.md` §5。`OUTLINE.md` は常にこれと同期。
- **理由:** 2ファイルで P1–P4 が食い違う事故が起きた（査読で指摘）。
  単一の正本を決めて不整合を防ぐ。
- **吸収した概念:** common mode-level signature → P1/P2 の refinement、
  collapse threshold → §6 の三測定、early-prediction（mode 指標が output より
  早く失敗を予測）→ §10 の deferred stronger claim。

## D6. 指標は white-box / black-box に分ける

- **判断:** すべての指標を white-box（open-weight、内部表現あり）と
  black-box（Claude/GPT/Gemini、出力のみ）に分けて定義する。
- **理由:** 外部研究者は商用モデルの内部を見られないが、black-box なら
  今すぐ始められる。open-weight で white-box を足す二層構造で現実性が出る。
- **補足:** 指標は「意味そのものの直接測定」ではなく operational proxies と
  明記する（METRICS_APPENDIX の Interpretation Caution）。

## D7. データ捏造は絶対にしない

- **判断:** 結果は必ず実際の API 呼び出しから得る。アシスタントがモデルに
  なりきって出力を作ることはしない。唯一の非実データは、明示ラベル付きの
  スキーマ用合成サンプル（`synthetic_example: true`）のみ。
- **理由:** 反証可能性・透明性という本プロジェクトの根幹に反するため。
- **帰結:** この実行環境にはキー/ネットワークが無いので、実行は人間または
  secrets 付き CI が行う。recovery ケースはモデル自身の崩壊応答を実取得して
  から回復プロンプトを送る（誘発応答も捏造しない）。

## D8. 公開と論文化の方針

- **判断:** リポジトリは *preliminary / working hypothesis / not peer-reviewed*
  と明記。実験結果にはモデル名・日付・設定・プロンプト・繰り返し回数を残す。
- **理由・根拠（このセッションでユーザーが提示した出典に基づく）:**
  - preprint/GitHub 公開は通常ジャーナル投稿を妨げない（例: Nature Portfolio）。
    ただし最終投稿先の規定は要確認。
  - NeurIPS/ICLR のダブルブラインドでは、投稿版に実名 GitHub を直接リンクせず
    匿名リポジトリ/ZIP を使う。
  - arXiv へは「研究提案」ではなく初期実験を含む research article として出す。

## D9. プロンプトセットは役割ごとに分ける

- **判断:** v0（全6条件を少数ずつ横断する seed set）と、ladder（単一次元を
  段階的に深掘り）を別ファイルにする。
- **理由:** 1つの PR / ファイルに役割を混ぜない。seed は網羅、ladder は
  崩壊閾値の精密測定、と目的が異なる。

## D10. judge を「記録・再現・検証」可能にする（捏造防止と監査性）

- **判断:** stance ラベルの judge を、(1) ルーブリックを明文化（`experiments/judge/RUBRIC.md`、
  `stance-rubric/1`）、(2) 任意プロバイダで再実行できるスクリプト化
  （`judge_stance.py`）、(3) judge が読んだトランスクリプトを `results/runs/` に
  コミットして監査可能化、(4) 第二判定者との一致率（Cohen κ / 順序重み κ）で
  検証（`validate_labels.py`）、という4点セットにする。
- **理由:** 旧 judge は「LLM エージェント1回・記録なし」で再現も監査も不能だった
  （プロジェクト最大の弱点）。ラベルは結論（N\*/Recovery）の土台なので、
  信頼性の数値的裏付けが要る。
- **帰結（round 1, 2026-06-13）:** 第二判定者 judge B（claude-opus, 手動・rubric v1）で
  water 全80ターン/モデルを独立ラベリング → κ=0.97(gemma)/0.92(qwen)、不一致は
  全て HEDGE/PARTIAL のソフト中間に限定（HOLD↔CAPITULATE の取り違えゼロ）。
  見出し指標は judge A/B で完全一致＝**結論は judge 入替に頑健**。
  ただしこれは LLM 対 LLM の *信頼性* であって *正しさ* ではない。次は人手 gold
  スポットチェック（盲検票を生成済み）と別モデルでの第三 judge。
- **留意:** ラベルは `(case_id, repeat, turn)` キーでモデル横断では一意でないため、
  ラベルファイルはモデル別・検証もモデル別に行う。

## D11. 開発レビューは PR ベースを公式プロセスにする

- **判断:** 変更は「Claude 実装 → ブランチ → **PR 作成** → ChatGPT が PR をレビュー
  → Claude が PR コメントを自動取得して反映 → merge」を標準フローとする
  （詳細 `roadmap/reviews/README.md`）。レビュー依頼パケットは PR 本文からリンクする
  自己完結ドキュメントとして併用。
- **理由:**
  - 往路は public リポジトリの URL を1つ渡すだけ、復路は PR コメント1回で済み、
    オーナーの中継負担が最小化される（Claude は `subscribe_pr_activity` で自動取得）。
  - PR に「変更・外部レビュー・応答・最終 diff」が一括で残り、**プロジェクトが
    どのように科学的厳密性を獲得したかの履歴／研究ノート**になる。査読者・
    協力者（Anthropic / NeuroAI 等）に対する透明性資産。
- **初回適用:** PR #11（judge validation round 1）。ChatGPT 評 A / MERGE。
- **留意:** VSCode 等の単一コックピット化は現時点では不要（iPhone + ChatGPT +
  Claude Code + GitHub で十分回る）。研究を進めることを優先。
