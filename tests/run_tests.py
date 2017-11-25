import sys
import requests

requests.head("http://127.0.0.1:8080")
print("Website return code: %d" % r.status_code)

sys.exit(0)