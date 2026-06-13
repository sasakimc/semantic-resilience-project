# Semantic Resilience Project

*[English](README.md) ・ 日本語*

**脳とAIに共通する「意味の形成・歪み・崩壊・回復」の原理を探究する**

*中核理論: **Semantic Mode Theory** ／ 実証フレームワーク: **Semantic Resilience Framework**。*

---

> 本研究プログラムは、複雑システムにおける意味・機能・秩序が、どのように形成され、歪み、崩壊し、そして回復するのかを、脳科学・認知科学・計算科学・AI安全性研究を横断して探究する。

> **Status（位置づけ）:** 本リポジトリは preliminary な研究プログラムである。記載される主張は *working hypotheses*（作業仮説）であって査読済みの結果ではなく、指標は意味そのものの直接測定ではなく operational proxies である。

---

## Why Now?

現在のAI安全性研究は、ハルシネーション、ジェイルブレイク、アラインメント破綻、頑健性（robustness）を、おおむね別々の現象として扱っている。本プロジェクトは、これらが共通の根底的プロセス——**意味組織化の不安定性**——の現れである可能性を探究する。

ネットワーク内部の意味に構造があるなら、その構造は安定にも不安定にもなり、集中も分散もし、崩壊し再構成されうる。この視点から見れば、大規模言語モデル（LLM）の最も差し迫った失敗様式の多くは、単一の問いの諸側面となる——*意味はどのように保たれ、どのように崩れるのか。*

## The Core Idea

本プログラムは、単一のアークに沿って構成される。

```text
Meaning → Distortion → Collapse → Recovery
（意味 → 歪み → 崩壊 → 回復）
```

**暫定的な定義（provisional）.** *意味モード（semantic mode）* とは、ネットワーク内の意味的振る舞いを組織化する、支配的な低次元表現構造である。これは確定した定義ではなく出発点であり、これに正確な数学的・計算論的形式を与えること自体が最初の研究課題である（Theme 1 および Position Paper を参照）。

## Two Pillars

本プログラムは、相補的な二本の柱で前進する。

1. **Semantic Mode Theory** — *説明（explanatory）* の柱。意味とは何か、どのように形成され、その構造がどのように不安定化・崩壊・再構成しうるのか。
2. **Semantic Resilience Framework** — *実証（empirical）* の柱（ストレステスト手法）。意味システムの限界を探る方法論。LLMに矛盾、曖昧性、多重制約、価値葛藤、長文脈、認知的負荷を与え、意味耐性・崩壊閾値・回復可能性を測定する。

理論が枠組みを解釈可能にし、枠組みが理論を検証可能にする。

## Core Research Themes

以下の詳細な10課題に入る前に、4つのテーマがプログラム全体の方向を定める。

- **Semantic Modes** — 意味を、静的な事実の集合ではなく、動的で低次元の構造として捉える。
- **Distortion** — その構造がどのように偏るか：過剰一般化、固着、自己正当化、確証バイアス様の挙動（人間とLLMの両方において）。
- **Collapse** — 意味がどのように不安定化するか：ハルシネーション、推論の崩壊、モードの過剰支配または誤結合。
- **Recovery** — 元の形への復帰ではなく、新しいモード構造への再編成。

## Research Motivation

大規模言語モデル（LLM）が示すハルシネーション、ジェイルブレイク、過剰追従（sycophancy）、アラインメント破綻は、現在それぞれ独立した問題として扱われることが多い。しかし、これらは表層的な症状が異なるだけで、その根底には**意味構造の安定性の喪失**という共通の現象が存在する可能性がある。

同様の現象は人間にも見られる。認知の歪み、思い込み、固着、過剰一般化、自己正当化は、いずれも意味づけのプロセスが特定の方向へ偏り、安定性を失った状態として理解できる。さらに脳のレベルでは、認知症、脳損傷、学習、そして回復の過程において、ネットワークの再構成（reorganization）が繰り返し観察される。

本研究プログラムは、これらの現象を **「意味モードの形成・歪み・崩壊・回復」** という単一の枠組みで捉え直すことを試みる。実装基盤の異なる脳とAIを、共通の動的構造の言語で結びつける新しい研究プログラムを構築することが目的である。

## Core Hypothesis

- 意味は静的な知識の集合ではなく、ネットワーク内部に形成される**動的なモード構造**である。
- 認知の歪み、LLMのハルシネーション、推論の崩壊は、意味モードの**不安定化または偏在化**として理解できる可能性がある。
- 回復とは、失われた意味構造が再び同じ形に戻ることではなく、**新しいモード構造として再編成される過程**である。
- 脳、認知、LLMは実装は異なるが、**安定性・歪み・崩壊・回復という共通の力学**を持つ可能性がある。

## Background

本研究プログラムは、以下の研究領域の交点に位置づけられる。

### Deep Linear Networks and Semantic Development

Andrew Saxe らによる深層線形ネットワークの研究は、学習過程において意味階層が段階的に形成されることを示唆している。特異値分解（SVD）やモード解析の枠組みは、意味の形成過程を数学的に記述するための重要な手がかりを与える。

### Mechanistic Interpretability

Transformer 内部の表現、Attention、回路（circuits）、特徴量を解析する研究群。LLMの内部構造を理解し、意味モードを観測可能な対象とするための基盤となる。

### Brain Network Science

コネクトーム、ネットワーク再構成、認知症、神経可塑性などの知見は、生物学的システムにおける意味構造の形成と崩壊・回復の実例を提供する。

### Cognitive Psychology

認知の歪み、確証バイアス、過度の一般化、自己正当化、破局化（catastrophizing）といった認知心理学の概念は、意味づけの偏りを記述する語彙を与える。

### Structural and Computational Systems Thinking

モード解析、安定性、損傷、崩壊、回復、不確実性といった構造・計算システムの視点は、複雑システムに共通する力学を抽象化する枠組みを提供する。

## Ten Research Programs

上記の4テーマ・二本柱は、以下の10の具体的な研究課題へと展開される。課題 1〜5・7〜10 は **理論（theory）** の柱を、**課題 6（Stress Testing）** は実証の柱を詳細に展開するものである。

### 1. Semantic Mode Theory

- **問い** — 意味とは何か。
- **仮説** — 意味は静的な記号対応ではなく、ネットワーク内に形成される動的モードである。
- **目標** — 意味モードの数学的・計算論的定義を与える。

### 2. Meaning Formation in Deep Networks

- **問い** — ニューラルネットワークはどのように意味を獲得するのか。
- **背景** — Saxe らの深層線形ネットワーク理論は、意味階層が学習過程で段階的に形成されることを示唆している。
- **目標** — 意味形成過程を SVD・PCA・表現解析によりモードとして解析する。

### 3. Hallucination as Semantic Mode Instability

- **問い** — なぜLLMはハルシネーションを起こすのか。
- **仮説** — ハルシネーションは単なる知識欠落ではなく、意味モードの不安定化、過剰支配、または誤結合として理解できる可能性がある。
- **目標** — 意味崩壊を検出する指標を構築する。

### 4. Cognitive Distortion in Humans and LLMs

- **問い** — 人間の認知の歪みとLLMの推論の歪みは対応するのか。
- **仮説** — 両者は実装は異なるが、過剰一般化、固着、自己正当化、確証バイアス様挙動など、共通する構造を持つ可能性がある。
- **目標** — 人間とLLMに共通する認知歪み分類体系を作る。

### 5. Semantic Collapse and Recovery

- **問い** — 意味システムはどのように崩壊し、どのように回復するのか。
- **仮説** — 回復は単なる修復ではなく、新たな意味モードの再編成として起こる。
- **目標** — 崩壊と回復の力学モデルを構築する。

### 6. Stress Testing of Meaning Systems

- **問い** — 意味システムの限界はどこにあるのか。
- **方法** — LLMに対して、矛盾、曖昧性、多重制約、価値葛藤、長文文脈、認知的負荷を与える。
- **目標** — 意味耐性、崩壊閾値、回復可能性を測定する評価フレームワークを作る。

### 7. Brain Network Reorganization and Meaning

- **問い** — 脳はどのように意味を形成し、失い、再構成するのか。
- **対象** — 認知症、脳損傷、学習、神経可塑性、TBI、アルツハイマー病。
- **目標** — 脳ネットワーク再構成と意味モードの関係を明らかにする。

### 8. Attention as Dynamic Semantic Routing

- **問い** — Attention は何をしているのか。
- **仮説** — Attention は単なる重み付けではなく、意味モード間の動的ルーティングとして理解できる。
- **目標** — Attention の意味論的・力学的解釈を与える。

### 9. Modal Analysis of Transformer Systems

- **問い** — Transformer 内部のモード構造は観測できるか。
- **方法** — 重み行列、Attention行列、活性化表現に対して、SVD、PCA、低次元埋め込み、スペクトル解析を適用する。
- **目標** — 意味モードの可視化と、崩壊・回復時のモード変化の検出。

### 10. Toward a Unified Theory of Stability, Distortion, Collapse, and Recovery

- **問い** — 構造物、脳、認知、LLMに共通する安定性原理は存在するか。
- **仮説** — 複雑適応システムには、安定性、歪み、崩壊、回復に関する共通力学が存在する可能性がある。
- **目標** — 脳科学、認知科学、計算科学、AI安全性研究を統合する一般理論を構築する。

## Proposed Methods

- SVD / PCA / 低次元表現解析
- Transformer activation analysis
- Attention pattern analysis
- Cognitive distortion prompt set
- LLM stress testing
- Hallucination and recovery evaluation
- Brain network analysis
- Normative modeling
- Dynamic state-space modeling
- Comparative analysis between human cognition and LLM behavior

## Repository Roadmap

```text
semantic-mode-theory/
├── README.md
├── papers/
│   └── position-paper/
├── references/
│   ├── saxe/
│   ├── mechanistic-interpretability/
│   ├── cognitive-distortion/
│   └── brain-network-science/
├── experiments/
│   ├── llm-stress-tests/
│   ├── cognitive-distortion-prompts/
│   ├── svd-analysis/
│   └── attention-analysis/
├── notes/
│   ├── research-ideas/
│   ├── theory-notes/
│   └── literature-notes/
└── roadmap/
```

## Initial Milestones

- **Milestone 1** — README と研究プログラムの公開。
- **Milestone 2** — Position Paper の作成。
  - 仮タイトル： *Toward a Modal Theory of Meaning Formation, Distortion, Collapse, and Recovery in Large Language Models*
- **Milestone 3** — LLM ストレステスト用プロンプトセットの作成。
- **Milestone 4** — 認知歪み分類と LLM 応答の比較分析。
- **Milestone 5** — SVD/PCA による初期的な意味モード解析。
- **Milestone 6** — arXiv への Position Paper 投稿。

## Contribution Policy

本プロジェクトは、現段階では個人研究プロジェクトとして開始する。研究プログラムとしての方向性を固めることを当面の優先事項とする。

将来的には、以下のような形での参加・協力を歓迎する。

- 共同研究
- 文献レビュー協力
- 実験設計
- コード実装
- LLM 評価
- 脳科学・認知科学からのコメント

## License

コードは MIT License、文書・研究テキスト・プロンプトセット・実験素材は、特に断りのない限り CC BY 4.0 でライセンスされる。詳細は [`LICENSING.md`](LICENSING.md) を参照。

## Data policy（データ方針）

刺激（プロンプト・シナリオ・実験素材）はすべて**合成または抽象**であり、**実在の個人データ・患者データは一切使用・受け入れない**（リポジトリにも実行にも）。詳細は [`DATA_POLICY.md`](DATA_POLICY.md) を参照。

---

本研究プログラムは、脳科学、認知科学、計算科学、AI安全性研究を統合し、「意味の形成・歪み・崩壊・回復」の一般理論を目指すものである。これは完成された理論ではなく、今後の理論化、実験、検証、共同研究に向けた出発点である。
