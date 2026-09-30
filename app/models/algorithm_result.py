from dataclasses import dataclass, field
from typing import Any


@dataclass
class AlgorithmResult:
    success: bool
    result: Any = None
    message: str = ""
    error: float | None = None
    iteration_count: int | None = None
    steps: list[str] = field(default_factory=list)
    table_columns: list[str] = field(default_factory=list)
    table_rows: list[list[Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def failure(cls, message: str, **fields: Any) -> "AlgorithmResult":
        return cls(success=False, message=message, **fields)
