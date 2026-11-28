"""Metadata completa usada pelo Alembic e pela criação do banco de testes."""

from app.db import audit  # noqa: F401
from app.db.base import Base
from app.modules.auth import models as auth_models  # noqa: F401
from app.modules.photos import models as photo_models  # noqa: F401
from app.modules.reflections import models as reflection_models  # noqa: F401
from app.modules.routes import models as route_models  # noqa: F401
from app.modules.teams import models as team_models  # noqa: F401
from app.worker import models as job_models  # noqa: F401

metadata = Base.metadata
