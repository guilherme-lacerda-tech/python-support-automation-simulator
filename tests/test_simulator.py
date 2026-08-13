from __future__ import annotations

from pathlib import Path

from python_support_automation_simulator.simulator import classify_ticket, run


def test_classify_ticket_routes_unmatched_to_manual_review() -> None:
    decision = classify_ticket({"ticket_id": "TCK-999", "category": "unknown", "priority": "low"}, [])

    assert decision["rule_id"] == "manual_review"
    assert decision["queue"] == "triage"


def test_run_persists_queue_and_history(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    result = run(
        root / "data" / "sample" / "tickets.json",
        root / "data" / "sample" / "rules.json",
        tmp_path / "support_simulator.db",
    )

    assert result["tickets"] == 3
    assert result["queues"] == {"data": 1, "operations": 1, "support": 1}
    assert result["history_entries"] == 3
