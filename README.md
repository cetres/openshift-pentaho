# openshift-pentaho
[![Build Status](https://travis-ci.org/cetres/openshift-pentaho.svg?branch=master)](https://travis-ci.org/cetres/openshift-pentaho)

```shell
$ oc new-app -f https://raw.githubusercontent.com/cetres/openshift-pentaho/master/template.yaml \
             -p APPLICATION_NAME=<application_name> \
             -p SERVER_USER=<server_user> \
             -p SERVER_PASSWD=<server_password> \
             -p SERVER_NAME=<application_url>
$ oc deploy <application_name>
```

## API
Documentation: https://help.pentaho.com/Documentation/7.1/0R0/070/020/020/030
