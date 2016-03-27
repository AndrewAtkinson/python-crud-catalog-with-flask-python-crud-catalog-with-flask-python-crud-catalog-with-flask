import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from werkzeug import secure_filename
from faker import Faker #sudo pip install fake-factory
from random import randrange

Base = declarative_base()

class Category(Base):
	__tablename__ = 'categories' 

	category_id = Column(Integer, primary_key=True)
	category_name = Column(String(250), nullable=False)


class CatalogItems(Base):
	__tablename__ = 'catalog_items' 

	item_id = Column(Integer, primary_key=True)
	item_title = Column(String(250), nullable=False)
	item_description = Column(Text)
	item_image = Column(String(250))
	item_deleted = Column(Boolean, default=False)
	category_id = Column(Integer, ForeignKey('categories.category_id'))
	category = relationship(Category)


class Database:
	def __init__(self):
		engine = create_engine('sqlite:///catalog.db')
		Base.metadata.create_all(engine)
		db_session = sessionmaker(bind=engine)
		self.db = db_session()

	def get_items(self):
		return self.db.query(CatalogItems).filter(CatalogItems.item_deleted == False).order_by("catalog_items.item_id desc").all()

	def get_item(self, item_id):
		return self.db.query(CatalogItems).filter(CatalogItems.item_id == item_id).one()

	def get_items_by_category_id(self, category_id):
		return self.db.query(CatalogItems).filter(CatalogItems.item_deleted == False).filter(CatalogItems.category_id == category_id).order_by("catalog_items.item_id desc").all()

	def add_item(self, request):
		uploaded_file = request.files['image']
		image = ''
		if uploaded_file.filename != '':
			filename = secure_filename(uploaded_file.filename)
			uploaded_file.save('images/' + filename)
			image = filename

		item = CatalogItems(
			item_title = request.form['title'],
			item_description = request.form['description'],
			item_image = image,
			category_id = request.form['category_id']
			)
		self.db.add(item)
		self.db.commit()

	def update_item(self, request):
		if request.form['item_id'] != '':
			item = self.get_item(request.form['item_id'])
			item.item_title = request.form['title']
			item.item_description = request.form['description']
			item.category_id = request.form['category_id']

			uploaded_file = request.files['image']
			if uploaded_file.filename != '':
				filename = secure_filename(uploaded_file.filename)
				uploaded_file.save('images/' + filename)
				item.item_image = filename

			self.db.add(item)
			self.db.commit()

	def delete_item(self, item_id):
		item = self.get_item(item_id)
		item.item_deleted = True
		self.db.add(item)
		self.db.commit()

	def get_categories(self):
		return self.db.query(Category).all()

	def get_category(self, category_id):
		return self.db.query(Category).filter(Category.category_id == category_id).one()

	def generate_categories(self):
		fake = Faker()
		for _ in range(0,10):
			category = Category(category_name = fake.word())
			self.db.add(category)
			item = CatalogItems(
			item_title = fake.word(),
			item_description = fake.sentence(),
			item_image = '',
			category_id = randrange(1, 10)			)
			self.db.add(item)

		self.db.commit()