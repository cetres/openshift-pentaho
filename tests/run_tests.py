import sys
import requests

try:
    r = requests.head("http://127.0.0.1:8080")
    print("Website return code: %d" % r.status_code)
except requests.RequestException as e:
    print(str(e))
    sys.exit(1)
sys.exit(0)
