\# LLM Practical Architecture Guide: Advanced Defense \& Context Engineering



\*\*Version:\*\* 1.0.0

\*\*Scope:\*\* Implementation patterns for multi-agent memory defense, information flow control (IFC), and hybrid formal verification.



\---



\## 1. マルチエージェント環境でのメモリ汚染防衛（低オーバーヘッド実装）



最もオーバーヘッドが少ないデザインパターンは\*\*「永続化レイヤー（Checkpointer / Memory Store）での一元的 scan-before-write」\*\*です。ノードやエージェントごとにバリデーションを分散させるのではなく、書き込みが収束する一点で強制します。



\### 推奨パターン：Guarded Checkpointer（LangGraph中心）



LangGraphの共有状態（checkpointer）が汚染の最大経路になるため、以下のようにラップします。



```python

from langgraph.checkpoint.base import BaseCheckpointSaver

from agent\_memory\_guard import MemoryGuard, Policy



class GuardedCheckpointer(BaseCheckpointSaver):

&#x20;   def \_\_init\_\_(self, base: BaseCheckpointSaver, policy=Policy.strict()):

&#x20;       self.base = base

&#x20;       self.guard = MemoryGuard(policy=policy)



&#x20;   def put(self, config, checkpoint, metadata, new\_versions):

&#x20;       # channel\_values 内のメッセージ／状態をスキャン

&#x20;       messages = checkpoint.get("channel\_values", {}).get("messages", \[])

&#x20;       for msg in messages:

&#x20;           content = getattr(msg, "content", "") or str(msg)

&#x20;           result = self.guard.scan(content)

&#x20;           if not result.is\_safe:

&#x20;               raise ValueError(f"ASI06 blocked: {result.threat\_type}")

&#x20;       return self.base.put(config, checkpoint, metadata, new\_versions)



&#x20;   # aput も同様に実装





コピペしやすいよう、通常のマークダウン形式で以下に記載いたします。



```markdown

\# LLM Practical Architecture Guide: Advanced Defense \& Context Engineering



\*\*Version:\*\* 1.0.0

\*\*Scope:\*\* Implementation patterns for multi-agent memory defense, information flow control (IFC), and hybrid formal verification.



\---



\## 1. マルチエージェント環境でのメモリ汚染防衛（低オーバーヘッド実装）



最もオーバーヘッドが少ないデザインパターンは\*\*「永続化レイヤー（Checkpointer / Memory Store）での一元的 scan-before-write」\*\*です。ノードやエージェントごとにバリデーションを分散させるのではなく、書き込みが収束する一点で強制します。



\### 推奨パターン：Guarded Checkpointer（LangGraph中心）



LangGraphの共有状態（checkpointer）が汚染の最大経路になるため、以下のようにラップします。



```python

from langgraph.checkpoint.base import BaseCheckpointSaver

from agent\_memory\_guard import MemoryGuard, Policy



class GuardedCheckpointer(BaseCheckpointSaver):

&#x20;   def \_\_init\_\_(self, base: BaseCheckpointSaver, policy=Policy.strict()):

&#x20;       self.base = base

&#x20;       self.guard = MemoryGuard(policy=policy)



&#x20;   def put(self, config, checkpoint, metadata, new\_versions):

&#x20;       # channel\_values 内のメッセージ／状態をスキャン

&#x20;       messages = checkpoint.get("channel\_values", {}).get("messages", \[])

&#x20;       for msg in messages:

&#x20;           content = getattr(msg, "content", "") or str(msg)

&#x20;           result = self.guard.scan(content)

&#x20;           if not result.is\_safe:

&#x20;               raise ValueError(f"ASI06 blocked: {result.threat\_type}")

&#x20;       return self.base.put(config, checkpoint, metadata, new\_versions)



&#x20;   # aput も同様に実装



```



\### 利点と追加の低コスト強化策



\* \*\*中央集中\*\*: 各エージェントノードを一切変更不要。

\* \*\*クロスセッション／クロスエージェント保護\*\*: 汚染が永続化される前に遮断。

\* \*\*オーバーヘッド\*\*: OWASP Agent Memory Guardは中央値 \*\*62µs\*\*（純Python・外部依存なし）。50並列スキャンでもp99 < 200µs程度。

\* \*\*信頼度パーティション\*\*: 共有書き込み可能なメモリを最小化。システム／ポリシー領域は読み取り専用。

\* \*\*プロビナンス署名\*\*: 書き込み時に `agent\_id + hash` を付与し、改ざん検知。



\---



\## 2. CaMeL / 情報フロー制御（IFC）の軽量Pythonランタイム構成



CaMeLの核心は、\*\*カスタムPythonインタプリタが値ごとにcapability（出所・許可メタデータ）を追跡し、ツール呼び出し時にポリシーを強制\*\*する点です。



\### 軽量ランタイムの構成例（概念）



from dataclasses import dataclass, field

from typing import Any, Set, Tuple

import ast



@dataclass

class Capabilities:

&#x20;   sources: Set\[str] = field(default\_factory=set)    # 出所（user, tool:email, ...）

&#x20;   readers: Set\[str] = field(default\_factory=set)    # 読み取り許可主体



@dataclass

class CaMeLValue:

&#x20;   value: Any

&#x20;   caps: Capabilities

&#x20;   deps: Tuple\["CaMeLValue", ...] = ()



class LightweightInterpreter:

&#x20;   def \_\_init\_\_(self, policy\_engine, q\_llm):

&#x20;       self.policy = policy\_engine

&#x20;       self.q\_llm = q\_llm          # 隔離LLM（ツール権限なし）

&#x20;       self.namespace = {}



&#x20;   def eval(self, code: str):

&#x20;       tree = ast.parse(code)

&#x20;       return self.\_eval\_node(tree)



&#x20;   def \_eval\_call(self, node):

&#x20;       # ツール呼び出し前にcapabilityを検査

&#x20;       kwargs = {k: self.\_eval\_node(v) for k, v in ...}

&#x20;       result = self.policy.check(tool\_name, kwargs)

&#x20;       if isinstance(result, Denied):

&#x20;           raise SecurityError(result.reason)

&#x20;       return CaMeLValue(raw\_result, new\_caps, deps=...)



\### 高速化のポイント



\* capabilityは `frozenset` で保持し、演算時は `union`（sources）／`intersection`（readers）のみ。

\* ポリシーは純粋Python関数（ツール名 + kwargs のcapsを見て allow/deny）。LLM呼び出しは不要。

\* P-LLMは「制限付きPythonコード」だけを生成し、生のツール出力は一切見ない。



\---



\## 3. 形式検証（Lean 4）と確率的LLMのリアルタイム接続



\### ボトルネックと実戦的な回避策・ハイブリッド設計



\* \*\*A. 実行時ガードレールとしてのLean（LeanGuardパターン）\*\*

\* ポリシーをLean 4で記述し、\*\*ツール呼び出しの直前\*\*に評価。

\* 評価手続き自体がLeanLTLセマンティクスと同等であると証明済み。

\* 拒否された呼び出しは「フィードバック」か「proof-guided repair」で修復。





\* \*\*B. オーケストレーション層の不変量だけを事前証明\*\*

\* トークン会計、予算上限、ステップ数制限などの\*\*ハーネス不変量\*\*をLeanで証明。日々のコード生成結果自体は証明せず、「ハーネスが壊れないこと」を保証。





\* \*\*C. 非同期／バッチ検証\*\*

\* リアルタイムパスでは軽量なランタイムチェック（型・スキーマ・ポリシー）のみ。重いLean証明はバックグラウンドやCIで実行。







\---



\## 4. 総合推奨アーキテクチャ



\[複数エージェント]

&#x20;       │

&#x20;       ▼

\[Guarded Checkpointer / Memory Guard]   ← 低オーバーヘッド（µs級）

&#x20;       │

&#x20;       ▼

\[Dual-LLM + Capability Interpreter]    ← データ／制御フロー分離

&#x20;       │

&#x20;       ▼

\[LeanGuard / 軽量ポリシーゲート]        ← ツール呼び出し直前の形式的チェック

&#x20;       │

&#x20;       ▼

\[サンドボックス実行]



