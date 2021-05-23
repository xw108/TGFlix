from sqlalchemy import Table,  Column,  Integer, String
from ..core import  metadata

genre = Table(
    "genre",
    metadata,
	Column('id', Integer, primary_key=True, index=True),
	Column( 'name', String, nullable=False),
	Column( 'slug', String, nullable=False),
	Column( 'desc', String),
	Column( 'cover_img', Integer),
)