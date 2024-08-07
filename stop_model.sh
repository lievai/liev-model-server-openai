#!/bin/bash
echo "Stopping model..."
pkill -f "python waitress_model_openai.py"
echo "Model stopped."
