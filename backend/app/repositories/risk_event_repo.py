from backend.app.models.risk_event import RiskEvent
from backend.app.repositories.base import BaseRepository

class RiskEventRepository(BaseRepository[RiskEvent]):
    pass

risk_event_repo = RiskEventRepository(RiskEvent)

