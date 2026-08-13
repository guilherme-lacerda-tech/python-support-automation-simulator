from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import json
from pathlib import Path

from python_support_automation_simulator.simulator import run


ROOT = Path(__file__).resolve().parents[1]
result = run(
    ROOT / "data" / "sample" / "tickets.json",
    ROOT / "data" / "sample" / "rules.json",
    ROOT / "data" / "generated" / "support_simulator.db",
)
print(json.dumps(result, indent=2))
