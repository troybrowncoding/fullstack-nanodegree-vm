# Item Catalog
Creates and maintains a database of items and categories accessible via an interactive web app.

## Files
* application.py -- Runs web server and web app
* database_setup.py -- Creates database and defines tables
* /static/styles.css -- Styling for web interface
* /templates -- HTML files for page generation

## Usage
Login to vagrant and run application.py from /vagrant/catalog to start the web server. The database will be created automatically if it does not already exist.
```bash
vagrant@vagrant-ubuntu-trusty-32:/vagrant/catalog$ python application.py
 * Running on http://0.0.0.0:5000/
 * Restarting with reloader

```
Open a web browser and access the app at [localhost:5000/](localhost:5000/)

JSON endpoints are available at:
* localhost:5000/categories/JSON -- List of all categories
* localhost:5000/categories/category_id/JSON -- List of all items in a category
* localhost:5000/categories/category_id/item_id/JSON -- List of an item's attributes

## Troubleshooting
Contact Troy at troybrowncoding@gmail.com if you have any issues or concerns.
