import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Category(Base):
	__tablename__ = 'category'

	id = Column(Integer, primary_key = True)
	name = Column(String(79), nullable = False)
	
	@property
	def serialize(self):
		# Returns data in serializable format
		return {
			'id' :self.id,
			'name' :self.name
		}

class Item(Base): 
	__tablename__ = 'item'

	id = Column(Integer, primary_key = True)
	name = Column(String(79), nullable = False)
	description = Column(String(255))
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)

	@property
	def serialize(self):
		# Returns data in serializable format
		return {
			'id' :self.id,
			'name' :self.name,
			'description' :self.description,
			'category_id' :self.category_id
		}


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
