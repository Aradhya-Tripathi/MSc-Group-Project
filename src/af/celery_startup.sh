#!/bin/bash

celery -A core worker --pool=prefork --loglevel=INFO -n AF-Predictions -Q AF-Predictions-Queue
