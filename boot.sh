#!/bin/bash
source venv/bin/activate
flask db upgrade
flask translate compile
python run.py