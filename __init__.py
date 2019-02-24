from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import make_response
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databaseSetup import Base, Category, Item
import random
import string
import json
import httplib2
import requests

app = Flask(__name__)

engine = create_engine('postgresql://dbuser:strongdbpassword@localhost/catalogitem')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalog')
def showCatalog():
    categories = session.query(Category)
    return render_template('catalog.html', categories=categories)


@app.route('/catalog/new', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newCategory.html')


@app.route('/catalog/<categoryName>/items')
def showCategory(categoryName):
    category = session.query(Category).filter_by(name=categoryName).one()
    items = session.query(Item).filter_by(categoryId=category.id)
    return render_template('showCategory.html', category=category, items=items)


@app.route('/catalog/<categoryName>/edit', methods=['GET', 'POST'])
def editCategory(categoryName):
    categoryToEdit = session.query(Category).filter_by(name=categoryName).one()
    if request.method == 'POST':
        categoryToEdit.name = request.form['name']
        session.add(categoryToEdit)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('editCategory.html',
                               category=categoryToEdit)


@app.route('/catalog/<categoryName>/delete', methods=['GET', 'POST'])
def deleteCategory(categoryName):
    categoryToDelete = session.query(Category).filter_by(name=categoryName)\
                                              .one()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteCategory.html',
                               category=categoryToDelete)


@app.route('/catalog/<categoryName>/items/new', methods=['GET', 'POST'])
def newItem(categoryName):
    category = session.query(Category).filter_by(name=categoryName).one()
    if request.method == 'POST':
        newItem = Item(name=request.form['name'],
                       description=request.form['description'],
                       category=category)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCategory', categoryName=category.name))
    else:
        return render_template('newItem.html', category=category)


@app.route('/catalog/<categoryName>/<itemName>')
def showItem(categoryName, itemName):
    category = session.query(Category).filter_by(name=categoryName).one()
    item = session.query(Item).filter_by(categoryId=category.id)\
        .filter(Item.name == itemName).one()
    return render_template('showItem.html', item=item)


@app.route('/catalog/<categoryName>/<itemName>/edit', methods=['GET', 'POST'])
def editItem(categoryName, itemName):
    category = session.query(Category).filter_by(name=categoryName).one()
    itemToEdit = session.query(Item).filter_by(categoryId=category.id)\
                                    .filter(Item.name == itemName).one()
    if request.method == 'POST':
        itemToEdit.name = request.form['name']
        itemToEdit.description = request.form['description']
        session.add(itemToEdit)
        session.commit()
        return redirect(url_for('showCategory',
                                categoryName=category.name))
    else:
        return render_template('editItem.html', category=category,
                               item=itemToEdit)


@app.route('/catalog/<categoryName>/<itemName>/delete',\
           methods=['GET', 'POST'])
def deleteItem(categoryName, itemName):
    category = session.query(Category).filter_by(name=categoryName).one()
    itemToDelete = session.query(Item).filter_by(categoryId=category.id)\
                                      .filter(Item.name == itemName).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showCategory',
                                categoryName=category.name))
    else:
        return render_template('deleteItem.html', category=category,
                               item=itemToDelete)


@app.route('/catalog.json')
def showCatalogJSON():
    jsonDict = {'Category': []}
    categories = session.query(Category).all()
    for category in categories:
        items = session.query(Item).filter_by(categoryId=category.id).all()
        jsonDict['Category'].append({'id': category.id,
                                     'name': category.name,
                                     'Item': []})
        for item in items:
            jsonDict['Category'][-1]['Item']\
                .append({'name': item.name,
                         'id': item.id,
                         'description': item.description,
                         'categoryId': item.categoryId})
    return jsonify(jsonDict)


@app.route('/catalog/<categoryName>/items/json')
def showCategoryJSON(categoryName):
    category = session.query(Category).filter_by(name=categoryName).one()
    items = session.query(Item).filter_by(categoryId=category.id)
    jsonDict = {'name': category.name, 'id': category.id, 'Item': []}
    for item in items:
        jsonDict['Item'].append({'name': item.name,
                                 'id': item.id,
                                 'description': item.description,
                                 'categoryId': item.categoryId})
    return jsonify(jsonDict)


@app.route('/catalog/<categoryName>/<itemName>/json')
def showItemJSON(categoryName, itemName):
    category = session.query(Category).filter_by(name=categoryName).one()
    item = session.query(Item).filter_by(categoryId=category.id)\
                              .filter(Item.name == itemName).one()
    return jsonify(item.serialize)



if __name__ == '__main__':
    app.debug = True
    app.run()
