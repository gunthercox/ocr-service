Development
===========

Running the container
---------------------

This application is fully Dockerized and can be started with docker compose.

.. code:: bash

   docker compose up -d

Running Tests
-------------

.. code:: bash

   docker compose exec app python -m unittest discover -s tests/

Running Linting Checks
----------------------

.. code:: bash

   docker compose exec app python -m flake8 ./

Build Documentation
-------------------

.. code:: bash

   docker compose exec app python -m sphinx -b html docs/ html
