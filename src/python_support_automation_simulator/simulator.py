from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy import delete, func, select

from .database import Base, create_engine_for_url
from .models import Action, History, QueueItem, Rule, Ticket


def classify_ticket(ticket: dict, rules: list[dict]) -> dict:
    for rule in rules:
        if ticket["category"] == rule["category"] and ticket["priority"] == rule["priority"]:
            return {"ticket_id": ticket["ticket_id"], "rule_id": rule["rule_id"], "queue": rule["queue"], "state": "queued"}
    return {"ticket_id": ticket["ticket_id"], "rule_id": "manual_review", "queue": "triage", "state": "queued"}


def run(tickets_path: Path, rules_path: Path, db_path: Path) -> dict:
    tickets = json.loads(tickets_path.read_text(encoding="utf-8"))
    rules = json.loads(rules_path.read_text(encoding="utf-8"))
    db_path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine_for_url(f"sqlite+pysqlite:///{db_path}")
    Base.metadata.create_all(bind=engine)
    from sqlalchemy.orm import sessionmaker

    SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    with SessionLocal() as session:
        session.execute(delete(History))
        session.execute(delete(QueueItem))
        session.execute(delete(Action))
        session.execute(delete(Rule))
        session.execute(delete(Ticket))
        session.add_all(Rule(**rule) for rule in rules)
        session.add_all(
            [
                Action(name="assign_queue", description="Place the ticket into a synthetic work queue."),
                Action(name="manual_review", description="Route unmatched tickets to synthetic manual triage."),
            ]
        )
        session.flush()

        for ticket in tickets:
            ticket_model = Ticket(
                ticket_id=ticket["ticket_id"],
                category=ticket["category"],
                priority=ticket["priority"],
                status=ticket["status"],
                message=ticket["message"],
            )
            session.add(ticket_model)
            session.flush()
            decision = classify_ticket(ticket, rules)
            session.add(
                QueueItem(
                    ticket_ref=ticket_model.id,
                    rule_id=decision["rule_id"],
                    queue=decision["queue"],
                    state=decision["state"],
                )
            )
            action_name = "assign_queue" if decision["rule_id"] != "manual_review" else "manual_review"
            session.add(
                History(
                    ticket_ref=ticket_model.id,
                    action=action_name,
                    from_state=ticket["status"],
                    to_state=decision["state"],
                    note=f"Matched rule {decision['rule_id']} and routed to {decision['queue']}.",
                )
            )
        session.commit()

        rows = session.execute(select(QueueItem.queue, func.count()).group_by(QueueItem.queue).order_by(QueueItem.queue)).all()
        history_entries = session.scalar(select(func.count(History.id))) or 0
    return {"tickets": len(tickets), "queues": dict(rows), "history_entries": history_entries}
