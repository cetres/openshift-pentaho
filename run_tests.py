import sys
import os
import logging
from xml.etree import ElementTree

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

import requests
from requests.auth import HTTPBasicAuth

SERVER_USER = os.environ.get("SERVER_USER", "admin")
SERVER_PASSWD = os.environ.get("SERVER_PASSWD", "admin")
BASE_URL = "http://127.0.0.1:8080"

TEST_FILE = "tests/null.kjb"
TEST_JOB = "null"

loglevel=os.environ.get("LOG_LEVEL", "INFO")
numeric_level = getattr(logging, loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=numeric_level)

logging.debug("HTTPBasicAuth User: %s Password: %s" % (SERVER_USER, SERVER_PASSWD))
auth = HTTPBasicAuth(SERVER_USER, SERVER_PASSWD)

job_id = None

try:
    logging.info("Test #1: Server status")
    url = urljoin(BASE_URL, "/kettle/status/?xml=Y")
    r = requests.get(url, auth=auth)
    logging.debug(r.content)
    if r.status_code == 200:
        tree = ElementTree.fromstring(r.content)
        status = {}
        for c in tree:
            status[c.tag] = c.text
        logging.info("Status: %s" % status["statusdesc"])
    else:
        logging.warm("Website returned code: %d" % r.status_code)



    logging.info("Test #2: Add a new Job")
    logging.debug("Loading job file %s..." % TEST_FILE)
    with open(TEST_FILE, "r") as f:
        job_file = f.read()
    url = urljoin(BASE_URL, "/kettle/addJob/?xml=Y")
    headers = {'Content-Type': 'application/xml'}
    r = requests.post(url, auth=auth, headers=headers, data=job_file)
    logging.debug(r.content)
    if r.status_code == 200:
        tree = ElementTree.fromstring(r.content)
        status = {}
        for c in tree:
            status[c.tag] = c.text
        if status["result"] == "OK":
            logging.info("Job submitted succesfully")
            logging.info("Server: %s" % status["message"])
            job_id = status["id"]
        else:
            logging.error("Error on Job submission")
            logging.error(r.content)
    else:
        logging.warm("Website returned code: %d" % r.status_code)


    logging.info("Test #3: Get Job status")
    url = urljoin(BASE_URL, "/kettle/jobStatus/?name=%s&id=%s&xml=Y" % (TEST_JOB, job_id))
    r = requests.get(url, auth=auth)
    logging.info(r.content)
    if r.status_code == 200:
        tree = ElementTree.fromstring(r.content)
        status = {}
        for c in tree:
            status[c.tag] = c.text
        logging.info("Job status: %s" % status["status_desc"])
    else:
        logging.warn("Website returned code: %d" % r.status_code)


    logging.info("Test #4: Run a Job")
    url = urljoin(BASE_URL, "/kettle/startJob/?name=%s&id=%s&xml=Y" % (TEST_JOB, job_id))
    r = requests.get(url, auth=auth)
    logging.debug(r.content)
    if r.status_code == 200:
        tree = ElementTree.fromstring(r.content)
        status = {}
        for c in tree:
            status[c.tag] = c.text
        if status["result"] == "OK":
            logging.info("Job submitted succesfully")
        else:
            logging.error("Error starting a job name %s" % TEST_JOB)
            logging.error(r.content)
    else:
        logging.warm("Website returned code: %d" % r.status_code)

except requests.RequestException as e:
    print(str(e))
    sys.exit(1)


sys.exit(0)
