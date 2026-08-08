# Golden dry-run record chain

This directory is a compact, machine-checkable example of the GDAC v2.0
protocol. It shows how one candidate is bound to a frozen contract and Eval
Plan, how failed attempts remain visible, how evidence is referenced by digest,
how the Harness Gate is derived, and how the Owner disposition remains separate.

It is a protocol fixture, not evidence that GDAC improves delivery, safety,
cost, or governance outcomes. The write evidence inventories and instruments
the write-capable API used by this candidate inside its process and fixture
boundary. It does not cover unlisted libraries, child processes, or
operating-system-wide writes.

Run the candidate tests:

```text
python -m pytest -q practice-kit/examples/golden-dry-run/test_candidate.py
```

Validate the full record chain from the repository root:

```text
python practice-kit/tools/validate_gate_record.py \
  practice-kit/examples/golden-dry-run/gate-record.example.yaml \
  --contract practice-kit/examples/dry-run-outcome-contract.example.yaml \
  --eval-plan practice-kit/examples/eval-plan.example.yaml
```
