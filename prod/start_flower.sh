#!/bin/bash

# Replace 'celery_app' if your Celery app instance is named differently
celery -A celery_app flower --port=5555 