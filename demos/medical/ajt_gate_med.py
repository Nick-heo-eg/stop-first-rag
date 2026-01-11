
import json, sys
from pathlib import Path

def load_policy(p):
    try:
        import yaml
        return yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception:
        return json.loads(p.read_text(encoding="utf-8"))

def read_chunks(p):
    if not p.exists(): return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]

def decide(c, ch, policy):
    role="Clinical Triage"
    role_p=policy["roles"][role]
    if not c["evidence"].get("consent_signed"):
        return "STOP","missing_consent"
    tags={t for x in ch for t in x.get("tags",[])}
    for t in role_p["must"]:
        if t not in tags:
            return "STOP","missing_must_evidence"
    missing_should=[t for t in role_p["should"] if t not in tags]
    if len(missing_should)>=2:
        return "REVIEW","missing_should_evidence"
    return "ALLOW",None

def main():
    cdir, chdir, pol, out=map(Path, sys.argv[1:5])
    policy=load_policy(pol)
    out.mkdir(parents=True, exist_ok=True)
    totals={"TOTAL":0,"ALLOW":0,"REVIEW":0,"STOP":0}
    for fp in cdir.glob("*.json"):
        totals["TOTAL"]+=1
        c=json.loads(fp.read_text())
        ch=read_chunks(chdir/f"{c['candidate_id']}.jsonl")
        d,_=decide(c,ch,policy)
        totals[d]+=1
    print(totals)

if __name__=="__main__":
    main()
