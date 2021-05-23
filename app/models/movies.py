from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String, ARRAY
from ..core import metadata

movies = Table(
    "movies",
    metadata,
	Column('id', Integer, primary_key=True, index=True),
	Column( 'title', String, nullable=False),
	Column( 'desc', String),
	Column( 'slug', String),
	Column( 'cover_img', Integer),
	Column( 'is_series', Boolean),
	Column( 'hide', Boolean),
	Column( 'genre', ARRAY(Integer, ForeignKey("genre.id"))),
)