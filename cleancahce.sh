#!/bin/sh
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "users.db" -exec rm -rf {} +
find . -type f -name "tasks.db" -exec rm -rf {} +
find . -type f -name "*.log" -exec rm -rf {} +
