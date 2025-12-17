# =============================================================================
# Configuration file for RAG Assistant
# =============================================================================
# Why a config file? 
# - Change settings in ONE place, not scattered across files
# - Easy to adjust for different environments (your laptop vs. server)
# - No "magic numbers/variables" buried in code
# =============================================================================

import os

# Default Configuration
DEFAULT_DB_PATH = "backend/database.duckdb" # UPDATE WITH YOUR .duckdb file for database.py
DEFAULT_TOP_K = 10 # Default top k neighbors parameter for app.py
DEFAULT_MAX_ITER = int(1e2) # Default iterations for app.py
DEFAULT_MODEL = "gpt-4o-mini" # Default model for app.py

# Model Options
AVAILABLE_MODELS = ["gpt-4.1", 
                    "gpt-4.1-mini", 
                    "gpt-4.1-nano", 
                    "gpt-4o",
                    "gpt-4o-mini", 
                    "gpt-4-turbo",
                    "gpt-4", 
                    "o1", 
                    "o1-mini"] # List of all available models for app.py

# Embedding Model
EMBEDDING_MODEL_NAME = "" # UPDATE TO YOUR MODEL
EMBEDDING_DIMENSION = 384 # UPDATE TO YOUR MODEL
