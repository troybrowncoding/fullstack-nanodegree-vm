
# import flask
from flask import (Flask, render_template, request, redirect,
	url_for, jsonify)
app = Flask(__name__)

# import database operations
from database_setup import Base, Category, Item
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to database
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Still to do:

# add message flashes for updates?
# add CSS
# add security/logins

@app.route('/categories/JSON')
def categoriesJSON():
	# JSON endpoint for list of categories
	categories = session.query(Category).all()
	return jsonify(Categories = [c.serialize for c in categories])

@app.route('/categories/<int:category_id>/JSON')
def categoryItemsJSON(category_id):
	# JSON endpoint for list of items in a category
	category = session.query(Category).filter_by(id = category_id).one()
	items = session.query(Item).filter_by(category_id = category.id)
	return jsonify(Items = [i.serialize for i in items])

@app.route('/categories/<int:category_id>/<int:item_id>/JSON')
def itemJSON(category_id,item_id):
	# JSON endpoint for a single item
	item = session.query(Item).filter_by(id = item_id).one()
	return jsonify(Item = item.serialize)

@app.route('/')
@app.route('/categories/')
def mainMenu():
	# Shows full list of categories
	items = session.query(Category).all()
	return render_template('mainMenu.html', items = items)

@app.route('/categories/<int:category_id>/')
def showCategory(category_id):
	# Shows items in a particular category
	category = session.query(Category).filter_by(id = category_id).one()
	items = session.query(Item).filter_by(category_id = category.id)
	return render_template('showCategory.html',
		category = category, items = items)

@app.route('/categories/new', methods=['GET','POST'])
def newCategory():
	# Creates a new category and displays it
	if request.method == 'POST':
		newCategory = Category(name = request.form['name'])
		session.add(newCategory)
		session.commit()
		return redirect(url_for('showCategory', category_id = newCategory.id))
	else:
		return render_template('newCategory.html')

@app.route('/categories/<int:category_id>/edit', methods=['GET','POST'])
def editCategory(category_id):
	# Edits a category and displays it
	editedCategory = session.query(
					 Category).filter_by(id = category_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedCategory.name = request.form['name']
		session.add(editedCategory)
		session.commit()
		return redirect(url_for('showCategory', category_id = category_id))
	else:
		return render_template('editCategory.html',
			category_id = category_id, i = editedCategory)

@app.route('/categories/<int:category_id>/delete', methods=['GET','POST'])
def deleteCategory(category_id):
	# Deletes a category and returns to the main menu
	itemsToDelete = session.query(Item).filter_by(
					category_id = category_id).all()
	categoryToDelete = session.query(
					   Category).filter_by(id = category_id).one()
	if request.method == 'POST':
		for item in itemsToDelete:
			session.delete(item)
		session.delete(categoryToDelete)
		session.commit()
		return redirect(url_for('mainMenu'))
	else:
		return render_template('deleteCategory.html', i = categoryToDelete)

@app.route('/categories/<int:category_id>/<int:item_id>')
def showItem(category_id, item_id):
	# Displays a particular item
	category = session.query(Category).filter_by(id = category_id).one()
	item = session.query(Item).filter_by(id = item_id).one()
	return render_template('showItem.html', category = category, item = item)

@app.route('/categories/<int:category_id>/new', methods=['GET','POST'])
def newItem(category_id):
	# Creates a new item within a category and displays it
	if request.method == 'POST':
		newItem = Item(name = request.form['name'],
			description = request.form['description'],
			category_id = category_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('showItem', category_id =
			category_id, item_id = newItem.id))
	else:
		return render_template('newItem.html', category_id = category_id)

@app.route('/categories/<int:category_id>/<int:item_id>/edit',
	methods=['GET','POST'])
def editItem(category_id, item_id):
	# Edits an item and displays it
	editedItem = session.query(
					 Item).filter_by(id = item_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.description = request.form['description']
		session.add(editedItem)
		session.commit()
		return redirect(url_for('showItem', category_id =
			category_id, item_id = item_id))
	else:
		return render_template('editItem.html',
			category_id = category_id, i = editedItem)

@app.route('/categories/<int:category_id>/<int:item_id>/delete',
	methods = ['GET', 'POST'])
def deleteItem(category_id, item_id):
	# Deletes an item and returns to its category
	itemToDelete = session.query(
					   Item).filter_by(id = item_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		return redirect(url_for('showCategory', category_id = category_id))
	else:
		return render_template('deleteItem.html', i = itemToDelete)

# Run server when executed
if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
