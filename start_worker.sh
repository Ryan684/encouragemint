#!/usr/bin/env bash
pip install -r backend/requirements.txt
celery -A backend worker --loglevel=info