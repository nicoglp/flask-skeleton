from datetime import datetime
from sqlalchemy import types, Column
from app.base.model import BaseDBModel

class PHIModel(BaseDBModel):

    __abstract__ = True

    owner_id = Column(types.String(36))

    created_at = Column(types.DateTime)
    modified_at = Column(types.DateTime)
    modified_by = Column(types.String(256))
