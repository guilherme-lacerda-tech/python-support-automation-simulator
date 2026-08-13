from __future__ import annotations

import json
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


def test_run_routes_unmatched_ticket_to_manual_review(tmp_path: Path) -> None:
    tickets = [
        {
            "ticket_id": "TCK-404",
            "created_at": "2026-01-10T10:00:00Z",
            "category": "billing",
            "priority": "low",
            "status": "open",
            "message": "Synthetic unmatched ticket.",
        }
    ]
    tickets_path = tmp_path / "tickets.json"
    rules_path = tmp_path / "rules.json"
    tickets_path.write_text(json.dumps(tickets), encoding="utf-8")
    rules_path.write_text("[]", encoding="utf-8")

    result = run(tickets_path, rules_path, tmp_path / "support_simulator.db")

    assert result["queues"] == {"triage": 1}
    assert result["history_entries"] == 1
