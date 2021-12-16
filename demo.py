from es_crawler import ES_CRALWER

HOST = " http://127.0.0.1"  # change your es host
PORT = "9200"  # change your es port
AUTH = "Basic YYYYYYYY=="  # change your es auth
crawler = ES_CRALWER(host=HOST, port=PORT, auth=AUTH)

query = "Select COUNT(1) FROM table"
crawler.run_sql(query=query)