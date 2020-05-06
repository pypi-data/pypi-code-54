from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID


@dataclass(frozen=True)
class PredictionContext:
    entity_id: UUID
    # There may be None in feature vector
    features: List[Optional[float]]
    request_body: str
    server_id: str
    # Support categorical output using str
    output: Union[float, str]
    created_at: datetime
