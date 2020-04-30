#!/usr/bin/env bash
pip install -r encouragemint/requirements.txt
celery -A encouragemint worker --loglevel=info