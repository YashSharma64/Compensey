#!/bin/bash

# Create models directory
mkdir -p models

# Check if data exists, if not create placeholder
if [ ! -f "data/zomato_clean.csv" ]; then
    echo "Data files not found. Creating placeholder data..."
    mkdir -p data
    # Create minimal placeholder data
    echo "review_text,rating,date" > data/zomato_clean.csv
    echo "Great service,5,2023-01-01" >> data/zomato_clean.csv
    echo "Average experience,3,2023-01-02" >> data/zomato_clean.csv
    
    echo "review_text,rating,date" > data/swiggy_clean.csv
    echo "Fast delivery,4,2023-01-01" >> data/swiggy_clean.csv
    echo "Poor packaging,2,2023-01-02" >> data/swiggy_clean.csv
fi

# Start the server
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
