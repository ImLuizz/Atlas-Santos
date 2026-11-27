from app.db.base import Base
from app.modules.auth import models as auth_models  # noqa: F401
from app.modules.teams import models as team_models  # noqa: F401

metadata = Base.metadata
