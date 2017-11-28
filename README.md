# openshift-pentaho
[![Build Status](https://travis-ci.org/cetres/openshift-pentaho.svg?branch=master)](https://travis-ci.org/cetres/openshift-pentaho)

```shell with right oc permissions
$ oc new-app -f https://raw.githubusercontent.com/cetres/openshift-pentaho/master/template.yaml \
             -p APPLICATION_NAME=<application_name> 
             -p SERVER_USER=<server_user> \
             -p SERVER_PASSWD=<server_password> \
             -p SERVER_NAME=<application_url>
$ oc start-build <application_name>
```