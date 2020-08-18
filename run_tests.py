#!/usr/bin/env python
import sys
import os
import logging
from xml.etree import ElementTree
from six.moves.urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth

SERVER_USER = os.environ.get("SERVER_USER", "admin")
SERVER_PASSWD = os.environ.get("SERVER_PASSWD", "admin")
BASE_URL = "http://127.0.0.1:8080"

TEST_FILE = "tests/null.kjb"


loglevel=os.environ.get("LOG_LEVEL", "INFO")
numeric_level = getattr(logging, loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=numeric_level)

logging.debug("HTTPBasicAuth User: %s Password: %s" % (SERVER_USER, SERVER_PASSWD))

class TestError(Exception):
    pass


class Carte(object):
    _base_url = None
    _auth = None
    _status = None
    
    @property
    def status(self):
        if self._status is None:
            self.get_status()
        return self._status["statusdesc"]
    
    def __init__(self, base_url, user, password):
        self._base_url = base_url
        self._auth = HTTPBasicAuth(SERVER_USER, SERVER_PASSWD)
        
    def get_status(self):
        url = urljoin(self._base_url, "/kettle/status/?xml=Y")
        r = requests.get(url, auth=self._auth)
        logging.debug(r.content)
        if r.status_code == 200:
            tree = ElementTree.fromstring(r.content)
            self._status = {}
            for c in tree:
                self._status[c.tag] = c.text
        else:
            logging.warm("Website returned code: %d" % r.status_code)

    def new_job(self, content):
        url = urljoin(self._base_url, "/kettle/addJob/?xml=Y")
        headers = {'Content-Type': 'application/xml'}
        r = requests.post(url, auth=self._auth, headers=headers, data=content)
        logging.debug(r.content)
        if r.status_code == 200:
            tree = ElementTree.fromstring(r.content)
            status = {}
            for c in tree:
                status[c.tag] = c.text
            return status
        else:
            logging.error("Website returned code: %d" % r.status_code)

    def job_status(self, job):
        url = urljoin(BASE_URL, "/kettle/jobStatus/?name=%s&id=%s&xml=Y" % (job.name, job.id))
        logging.debug("Get job status")
        r = requests.get(url, auth=self._auth)
        logging.debug(r.content)
        if r.status_code == 200:
            tree = ElementTree.fromstring(r.content)
            status = {}
            for c in tree:
                status[c.tag] = c.text
            return status
        else:
            logging.error("Website returned code: %d" % r.status_code)

    def run_job(self, job):
        url = urljoin(BASE_URL, "/kettle/startJob/?name=%s&id=%s&xml=Y" % (job.name, job.id))
        r = requests.get(url, auth=self._auth)
        logging.debug(r.content)
        if r.status_code == 200:
            tree = ElementTree.fromstring(r.content)
            status = {}
            for c in tree:
                status[c.tag] = c.text
            return status
        else:
            logging.warm("Website returned code: %d" % r.status_code)
            
class Job(object):
    _id = None
    _name = None
    _server = None
    _deploy_status = None
    _content = None

    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def deploy_message(self):
        return self._deploy_status["message"]
    
    @property
    def status(self):
        return self._server.job_status(self)
    
    @property
    def deployed(self):
        return True if self._deploy_status["result"] == "OK" else False
    
    def __init__(self, server, filename):
        self._server = server
        logging.debug("Loading job file %s..." % filename)
        with open(filename, "r") as f:
            self._content = f.read()
        self._name = self.get_job_name(self._content)
        self._deploy_status = self._server.new_job(self._content)
        if self._deploy_status["result"] == "OK":
            self._id = self._deploy_status["id"]
        else:
            logging.error("Error on Job submission")
            logging.error(self._status["message"])
    
    def get_job_name(self, xml_content):
        tree = ElementTree.fromstring(xml_content)
        if tree.tag != "job_configuration":
            logging.error("Job XML root tag is not job_configuration")
            raise TestError("Job XML root tag is not job_configuration")
        name = None
        for c in tree:
            for c2 in c:
                if c2.tag == "name":
                    name = c2.text
        return name

    def run(self):
        status = self._server.new_job(self._content)
        if status["result"] == "OK":
            logging.info("Job started succesfully")
        else:
            logging.error("Error starting a job name %s" % TEST_JOB)
            logging.error(r.content)


try:
    carte = Carte(BASE_URL, SERVER_USER, SERVER_PASSWD)
    logging.info("Test #1: Server status")
    logging.info("Status: %s" % carte.status)

    logging.info("Test #2: Add a new Job: %s" % TEST_FILE)
    job = Job(carte, TEST_FILE)
    if job.deployed:
        logging.info("Job %s succesfully submitted" % job.name)
        logging.info("Server response: %s" % job.deploy_message)
    
        logging.info("Test #3: Get Job status")
        logging.info("Job status: %s" % job.status)

        logging.info("Test #4: Run a Job")
        status = job.run()
    else:
        logging.info("Error adding new job")
        sys.exit(1)
    
except requests.RequestException as e:
    logging.error(str(e))
    sys.exit(1)
except TestError as e:
    logging.error(str(e))
    sys.exit(2)
