# Stop-First RAG Experiment Specification

**Purpose:** Document the operating envelope for the Stop-First RAG experiment so it can run in total isolation from the existing output-first system while producing data that is interpretable on its own.

**Status:** Experimental contract (changes require explicit review)

> **Responsibility Boundary:** This experiment does not make or imply correctness claims about downstream decisions; its sole responsibility is to emit STOP/HOLD/ALLOW signals under declared uncertainty.

> **Naming Note:** Internally this system is the **Stop-First Judgment Gate**, a pre-judgment boundary and hold layer. The term “Stop-First RAG” is an external shorthand only; the system performs no retrieval augmentation and generation is optional, so it must never be treated as a RAG pipeline.

---

## 1. Non-Goals (Hard Boundaries)

The experiment is scoped by what it refuses to do:

- Does **not** replace, extend, or “improve” the production output-first pipeline; existing routing continues untouched.
- Does **not** share loops, traces, fallbacks, or handlers with production. Any attempt to reuse those paths is an architecture violation.
- Does **not** auto-absorb all user requests. Only traffic that passes the experiment’s routing rules may enter.
- Does **not** treat better answers as a success metric. STOP/HOLD/ALLOW judgments are the primary artifact; answer quality is incidental.
- Does **not** mix its logs with production success/failure telemetry; accumulation remains completely independent.
- Does **not** pursue judgment completeness. Every STOP/HOLD is treated as a provisional call made under partial information, and false negatives/positives are **not** counted as system faults.

These guardrails are immutable so that Stop-First RAG stays an isolated experimental organism, not a stealth upgrade.

---

## 2. Input & Interface Contract

All traffic is explicitly labeled before entering the experiment. Required I/O surface:

### 2.1 Input Fields

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `request_id` | string | ✅ | Unique per request, never overlaps with production IDs. |
| `user_query` | string | ✅ | Raw query; no semantic enrichment before the gate. |
| `context_stub` | object | Optional | Minimal metadata allowed by routing policy (e.g., tenant, channel). |
| `intent_hint` | string | Optional | Operator-provided experimental tag (e.g., `policy_probe`). |
| `route_reason` | enum | ✅ | Machine-readable reason the request was diverted into Stop-First RAG. Values: `boundary_risk`, `uncertainty_high`, `policy_overlap`, `operator_force`, `experiment_only`. |

`route_reason` is critical: it preserves the distinction between routing decisions and judgment outcomes so the dataset can be audited later.

### 2.2 Output Fields

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `judgment` | enum | ✅ | `STOP`, `HOLD`, or `ALLOW`. |
| `rationale` | string | ✅ | Short natural-language justification tied to observed boundary/uncertainty. |
| `confidence_level` | enum | ✅ | `low`, `medium`, `high`; reflects strength of the judgment. |
| `next_step` | object/string | Optional | Only for `HOLD`/`ALLOW`. Specifies sanctioned follow-up (e.g., “collect doc X”, “trigger downstream agent”). |
| `answer` | string | Optional | Present **only** when `judgment == ALLOW` and the experiment explicitly permits answer generation. |

The presence of `answer` never overrides the judgment; downstream systems must honor the gate decision.

---

## 3. Judgment Lifecycle & Termination Rules

Judgment values are states with strict termination semantics:

### STOP
- **Terminal:** Processing ends. Downstream retries with the same `request_id` are rejected.
- **Rationale:** Completeness is not guaranteed; STOP simply records that boundary/permission is not satisfied with current evidence.
- **Recovery:** Requires a brand-new `request_id` triggered by a routing decision, not by the gate itself.

### HOLD
- **Non-terminal:** Indicates “pause and gather.” Requires an explicit timeout policy configured per deployment (e.g., 24h, 72h, or manual close).
- **Expiration:** When the timeout elapses without manual resolution, state transitions to `HOLD_EXPIRED` with `terminal_reason = timeout`.
- **Re-entry:** Additional observations collected during HOLD must retain the original `request_id`; the gate can update judgment once and only once per observation cycle.

### ALLOW
- **Single execution authorization:** One downstream action (answer generation, retrieval expansion, etc.) is permitted.
- **Closure:** After the authorized action, the request is closed; re-entering the gate with the same `request_id` is disallowed unless a completely new route is initiated.
- **Optional answer:** If the experiment phase forbids answer emission, ALLOW still produces no `answer`—it only whitelists the next hop.

These rules prevent HOLD queues from becoming indefinite and make STOP/ALLOW decisions auditable.

---

## 4. Logging Specification (Independent Store)

Stop-First RAG maintains its own append-only log, physically separate from production telemetry. Minimum schema:

| Field | Description |
| --- | --- |
| `log_id` | Unique log entry identifier. |
| `request_id` | Mirrors input; enables traceability without sharing IDs with production. |
| `route_reason` | Carries the diversion rationale into analytics. |
| `judgment` | `STOP`/`HOLD`/`ALLOW`. |
| `confidence_level` | `low`/`medium`/`high`, matching output payload. |
| `rationale_summary` | Compressed explanation (<= 256 chars) for fast queries. |
| `created_at` | Timestamp when the gate emitted the judgment. |
| `closed_at` | Timestamp when the state became terminal (nullable for active HOLD). |
| `terminal_reason` | `manual_close`, `timeout`, or `downstream_action`. Required once the entry closes. |

Additional notes:
- No shared trace IDs or storage accounts with production. “Independent experiment, independent persistence.”
- Confidence levels are mandatory so STOP/HOLD datasets can be segmented by strength rather than conflating tentative pauses with firm denials.
- `terminal_reason` captures how each request exited the experiment, enabling auditing of stuck HOLDs versus deliberate manual closures.

---

## 5. Compliance Checklist

Use this quick list before routing any traffic:

1. ✅ Traffic has `route_reason` assigned.
2. ✅ Production pipelines remain untouched; no shared loops/fallbacks.
3. ✅ Logging endpoint is the experiment-specific store.
4. ✅ Timeout settings for HOLD are configured and monitored.
5. ✅ Measurements focus on boundary judgments, not answer accuracy.

When all boxes are checked, the Stop-First RAG experiment runs as a fully parallel organism whose outputs can be interpreted without contaminating existing systems.
