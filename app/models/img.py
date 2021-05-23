from sqlalchemy import Table, Column, ForeignKey, Integer
from ..core import metadata


img = Table(
	"images",
    metadata,
	Column('id', Integer, primary_key=True, index=True),
	Column('ch_id', Integer,ForeignKey('channels.id'), index=True, nullable=False),
	Column('msg_id', Integer, index=True, nullable=False),
)
