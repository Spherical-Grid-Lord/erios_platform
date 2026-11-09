# ERIOS Governance Protocol (EGP) v2.0 Enterprise - Detailed Design v1

## 1. リポジトリ構成 (Monorepo)
- governance/
- schema/ (egp.schema.json, policy.schema.json, route.schema.json, fruit.schema.json)
- kernel/ (state_machine/, policy_engine/, provenance/, audit/)
- tree_governor/
- layer_governor/
- tsumugi/
- verification/ (consistency/, topology/, drift/, invariant/, jepa/)
- graph/
- registry/
- federation/
- api/
- runtime/
- storage/
- deployment/

## 2. マイクロサービス設計
- **governance-kernel**: State Machine, Policy, Trace, Audit
- **tree-governor**: Tree管理, Fruit管理, Rework管理
- **layer-governor**: L1-L5分離, Provenance管理
- **tsumugi-runtime**: 推論, Route決定, 仮説生成
- **verification-core**: JEPA, Invariant, Topology, Drift
- **fruit-registry**: 成果物保管

## 3. データベーススキーマ概要
- ruit_registry: 成果物のバージョンおよび品質レベル（F0〜F5）管理
- ework_registry: 失敗履歴、根本原因、再発防止策の蓄積
- governance_events: 監査ログ、トレーサビリティイベント（JSONB対応）
