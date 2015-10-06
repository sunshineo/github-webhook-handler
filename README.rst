Flask webhook for Github and Tutum
########################
A very simple github post-receive web hook handler that redeploy a tutum service.

It will also verify that the POST request originated from github.com or a
defined GitHub Enterprise server.

Gettings started
----------------

Installation Requirements
=========================

Install dependencies found in ``requirements.txt``.

.. code-block:: console

    pip install -r requirements.txt

Runtime Configuration
=====================

Runtime operation is influenced by a set of environment variables which require
being set to influence operation.  Only SERVICE_MAP is required to be set.  The
remaining variables are optional.  USE_PROXYFIX needs to be set to true if
being used behind a WSGI proxy, and is not required otherwise.  GHE_ADDRESS
needs to be set to the IP address of a GitHub Enterprise instance if that is
the source of webhooks.

Set environment variable for the tutum service to re-deploy.

.. code-block:: console

    export SERVICE_MAP={"master":"b7a93ffb-4bb7-4d7c-8319-825131b03889","dev":"12b70a61-fc21-4c20-b043-2859f5489d2b"}

Start the server behind a proxy (see:
http://flask.pocoo.org/docs/deploying/wsgi-standalone/#proxy-setups)

.. code-block:: console

    USE_PROXYFIX=true python index.py 8080

Start the server to be used with a GitHub Enterprise instance.

.. code-block:: console

   GHE_ADDRESS=192.0.2.50 python index.py 80

Start the server.
=================
.. code-block:: console

    python index.py 80

Run using docker
================
.. code-block:: console

    docker run -e SERVICE_MAP={"master":"b7a93ffb-4bb7-4d7c-8319-825131b03889","dev":"12b70a61-fc21-4c20-b043-2859f5489d2b"} tutum.co/sunshineo/github-webhook-handler

Go to your repository's settings on `github.com <http://github.com>`_ or your
GitHub Enterprise instance and register your public URL under
``Service Hooks -> WebHook URLs``.
