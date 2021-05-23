from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String
from ..core import metadata

tempdata = Table(
	"temp_data",
    metadata,
	Column('id', Integer, primary_key=True, index=True),
	Column('c_id', Integer,ForeignKey('channels.id'), index=True, nullable=False),
	Column( 'm_id', Integer,ForeignKey('movies.id'), nullable=False),
	Column( 'ses', Integer),
	Column( 'slug_base', String, nullable=False),
	Column( 'is_series', Boolean),
)
