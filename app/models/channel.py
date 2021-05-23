from sqlalchemy import Table, Column, Integer, String
from ..core import metadata


tgchannel = Table(
	"channels",
    metadata,
	Column('id', Integer, primary_key=True, index=True),
	Column('channel_id', Integer, index=True, nullable=False)
)
