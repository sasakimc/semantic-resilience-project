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

- **判断:** Semantic Mode Theory（説明）と Stress Testing Framework（実証）の
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
