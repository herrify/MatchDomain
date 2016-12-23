#!/usr/bin/env python3

templete = {
    'login': 'ssh -p {PORT} {USER}@{HOST}',
    'query': 'ssh -p {PORT} {USER}@{HOST} query_cmd',
    'upload': 'ssh -p {PORT} {USER}@{HOST} upload_cmd',
    'chpass': 'ssh -p {PORT} {USER}@{HOST} chpass_cmd',
}

instance = dict((key, templete.get(key).format(PORT=100, USER='root', HOST='127.0.0.1')) for key in templete)

print(instance)

