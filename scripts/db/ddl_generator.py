import os
os.environ["UBIOME_ENVIRONMENT"] = "development"

from sqlalchemy.schema import CreateTable

from app import db

#  Dump schema to Kit module
from app.kits.model import *

print CreateTable(KitType.__table__).compile(db.engine)
print CreateTable(Kit.__table__).compile(db.engine)

