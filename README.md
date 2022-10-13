# PPR501 assignment (#MSE10HN Group 8)
* Create a student management website (CRUD).
* Create an API endpoint to get data for one student only (GET /students/:id).
* Create a crawler to crawl data from Student List page => Pretty-save to a text file.

# Usages
First, make sure you have Python 3.7+. You also need to install all required dependencies:
```
pip install -r requirements.txt
```

To initialize SQLite DB (with no data):
```
python main.py initdb
```

To start server:
```
python main.py startserver
```

With auto-reload:
```
python main.py startserver --dev
```

To run standalone crawler: First brings up the server, then open another terminal and run the following command:
```
python main.py crawl [--output=<output_file>]
```
The default output file will be `students.txt`

It is possible to get the crawled file by accessing `http://localhost:8000/crawling/students`

To access student list page: Access `http://localhost:8000/students/list`

