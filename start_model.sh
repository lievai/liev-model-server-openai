#!/bin/bash
echo "Starting model..."
nohup python waitress_model_openai.py > ./logs/waitress_model_openai.log 2>&1 &
echo "Model started."
