### ORIGINAL TASK
Mister Tony Stark received a file in which all working times in minutes of all employees were
gathered. The file is a bit chaotic.
Mister Stark wants to upload his file to an API which returns him a CSV or JSON file
describing how many hours each employee has worked. It is very likely that mister Stark
would like to have different output file formats in the future.
##### The input file looks like that:
philipp:300 ,maurice:221, lisa:112, philipp:123,felix:300,
maurice:-221,Hanna:112,Philipp:123,mauricE:-13
##### Requirements:
- ability to import the file via an API
- all names are not case sensitive
- the output should be sorted descended by working time
- the output should be extendable with additional statistics for example avg. working time

### Additional Assumption
Negative time worked not possible, so these are converted to positive values


1. Install requirements
```bash
pip install -r requirements.txt
```

2. Run the applications
```
python manage.py runserver
```

3. Open "http://127.0.0.1:8000"

4. Menu option:
###Create CSV from file and displays as JSON:
"download/csv": "http://127.0.0.1:8000/download/csv/" 
###Create JSON from file and displays as JSON:
"download/json": "http://127.0.0.1:8000/download/json/",
###View as JSON from file with not file created:
"view/json": "http://127.0.0.1:8000/view/json/"

5. Click option and upload file