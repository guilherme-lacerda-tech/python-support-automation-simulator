from __future__ import annotations

import json
import sqlite3
from pathlib import Path


def classify_ticket(ticket: dict, rules: list[dict]) -> dict:
    for rule in rules:
        if ticket["category"] == rule["category"] and ticket["priority"] == rule["priority"]:
            return {"ticket_id": ticket["ticket_id"], "rule_id": rule["rule_id"], "queue": rule["queue"], "state": "queued"}
    return {"ticket_id": ticket["ticket_id"], "rule_id": "manual_review", "queue": "triage", "state": "queued"}


def run(tickets_path: Path, rules_path: Path, db_path: Path) -> dict:
    tickets = json.loads(tickets_path.read_text(encoding="utf-8"))
    rules = json.loads(rules_path.read_text(encoding="utf-8"))
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute("create table if not exists tickets(ticket_id text, category text, priority text, status text)")
        conn.execute("create table if not exists queue(ticket_id text, rule_id text, queue text, state text)")
        conn.execute("delete from tickets")
        conn.execute("delete from queue")
        for ticket in tickets:
            conn.execute("insert into tickets values (?, ?, ?, ?)", (ticket["ticket_id"], ticket["category"], ticket["priority"], ticket["status"]))
            decision = classify_ticket(ticket, rules)
            conn.execute("insert into queue values (?, ?, ?, ?)", (decision["ticket_id"], decision["rule_id"], decision["queue"], decision["state"]))
        rows = conn.execute("select queue, count(*) from queue group by queue order by queue").fetchall()
    return {"tickets": len(tickets), "queues": dict(rows)}
