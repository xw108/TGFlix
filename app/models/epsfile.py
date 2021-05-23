from sqlalchemy import Table, Boolean, Column, Integer, String, TIMESTAMP
from ..core import metadata

epFile = Table(
    "files",
    metadata,
	Column('id', Integer, primary_key=True, index=True),
	Column( 'msg_id', String, index=True, nullable=False),
	Column( 'ch_id', String, nullable=False),
	Column( 'slug', String, nullable=False, index=True),
	Column( 'qlty', String),
	Column( 'movie_id', Integer, nullable=False),
	Column( 'ses', Integer),
	Column( 'eps', Integer),
	Column( 'size', String),
	Column( 'upd_at', TIMESTAMP),
	Column( 'downs', Integer),
	Column( 'hide', Boolean),
)