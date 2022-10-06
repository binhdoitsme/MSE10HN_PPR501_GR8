# PPR501 assignment (#MSE10HN Group 8)
* Create a student management website (CRUD).
* Create an API endpoint to get data for one student only (GET /students/:id).
* Create a crawler to crawl data from Student List page => Pretty-save to a text file.

# Usages
First, make sure you have Python 3.7+. You also need to install all required dependencies:
```pip install -r requirements.txt```

To initialize SQLite DB (with no data):
```python main.py initdb```

To start server:
```python main.py startserver```

With auto-reload:
```python main.py startserver --dev```


