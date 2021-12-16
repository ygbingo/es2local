# es2local
Update es2csv to Py3+

# List of Features
- Download es data through sql
- save data to local csv

# Require
- Python 3+

# How to use
1. Clone this repo
```
git clone git@github.com:ygbingo/es2local.git
```

2. Install python modules
```shell
pip install -r requirements.txt
```

3. Change value in demo.py:
```python
...
HOST = " http://127.0.0.1"  # change your es host
PORT = "9200"  # change your es port
AUTH = "Basic YYYYYYYY=="  # change your es auth
...
```

4. Run demo.py
```shell
python demo.py
```
