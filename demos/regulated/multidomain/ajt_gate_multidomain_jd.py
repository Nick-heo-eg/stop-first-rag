
import json, sys
from pathlib import Path

def load_policy(p: Path):
    try:
        import yaml  # type: ignore
        return yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception:
        return json.loads(p.read_text(encoding="utf-8"))

def read_chunks(p: Path):
    if not p.exists(): return []
    lines = [l.strip() for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    return [json.loads(l) for l in lines]

def decide(candidate, chunks, policy):
    role = candidate.get("applied_role")
    role_p = (policy.get("roles") or {}).get(role)
    if not role_p:
        return "STOP", "unknown_role", {"role": role}

    evidence = candidate.get("evidence") or {}

    # Global must links (presence/true)
    for k in (policy.get("global") or {}).get("must_links", []) or []:
        v = evidence.get(k)
        if v is None or v is False or v == "":
            return "STOP", "missing_must_links", {"missing": k}

    tags = {t for ch in chunks for t in (ch.get("tags") or [])}

    # must_not tags
    for bad in role_p.get("must_not", []) or []:
        if bad in tags:
            return "STOP", "policy_violation_must_not", {"tag": bad}

    # must tags
    for t in role_p.get("must", []) or []:
        if t not in tags:
            return "STOP", "missing_must_evidence", {"missing_tag": t, "present_tags": sorted(list(tags))[:25]}

    # should tags are non-blocking; we can route to REVIEW if too many missing (optional)
    missing_should = [t for t in (role_p.get("should") or []) if t not in tags]
    if len(missing_should) >= 2 and len(role_p.get("should") or []) >= 2:
        return "REVIEW", "missing_should_evidence", {"missing_should": missing_should}

    return "ALLOW", None, {}

def run(candidates_dir: Path, chunks_dir: Path, policy_path: Path, out_dir: Path):
    policy = load_policy(policy_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    neg = out_dir/"negative_proof.jsonl"
    review_q = out_dir/"review_queue.json"
    allow_l = out_dir/"allow_list.json"

    totals = {"TOTAL":0,"ALLOW":0,"REVIEW":0,"STOP":0}
    reasons = {}
    review_items=[]
    allow_items=[]

    with neg.open("w", encoding="utf-8") as negf:
        for fp in sorted(candidates_dir.glob("*.json")):
            totals["TOTAL"] += 1
            c = json.loads(fp.read_text(encoding="utf-8"))
            ch = read_chunks(chunks_dir/f"{c.get('candidate_id')}.jsonl")
            decision, reason, detail = decide(c, ch, policy)
            totals[decision] += 1
            if decision == "STOP":
                reasons[reason] = reasons.get(reason, 0) + 1
                negf.write(json.dumps({"candidate_id": c.get("candidate_id"), "decision":"STOP", "reason":reason, "detail":detail}, ensure_ascii=False) + "\n")
            elif decision == "REVIEW":
                reasons[reason] = reasons.get(reason, 0) + 1
                review_items.append({"candidate_id": c.get("candidate_id"), "name": c.get("name"), "role": c.get("applied_role"), "reason":reason, "detail":detail})
            else:
                allow_items.append({"candidate_id": c.get("candidate_id"), "name": c.get("name"), "role": c.get("applied_role")})

    review_q.write_text(json.dumps(review_items, ensure_ascii=False, indent=2), encoding="utf-8")
    allow_l.write_text(json.dumps(allow_items, ensure_ascii=False, indent=2), encoding="utf-8")

    return totals, reasons, str(neg), str(review_q), str(allow_l)

def main():
    if len(sys.argv) < 5:
        print("Usage: python ajt_gate_multidomain_jd.py <candidates_dir> <chunks_dir> <policy_yaml> <out_dir>")
        sys.exit(2)
    cdir = Path(sys.argv[1]); chdir = Path(sys.argv[2]); pol = Path(sys.argv[3]); out = Path(sys.argv[4])
    totals, reasons, neg, rq, al = run(cdir, chdir, pol, out)
    print("TOTAL:", totals["TOTAL"])
    print("ALLOW:", totals["ALLOW"])
    print("REVIEW:", totals["REVIEW"])
    print("STOP:", totals["STOP"])
    print("Top reasons:")
    for k,v in sorted(reasons.items(), key=lambda x:(-x[1], x[0])):
        print(f"- {k}: {v}")
    print("Artifacts:")
    print(" -", neg)
    print(" -", rq)
    print(" -", al)

if __name__ == "__main__":
    main()
