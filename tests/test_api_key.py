#!/usr/bin/env python
"""Test script to verify API key is being read correctly."""
import os
from src.core.ai_director import AIDirector

print("=" * 60)
print("Testing Google API Key Configuration")
print("=" * 60)

# Check environment variable
env_key = os.getenv('GOOGLE_API_KEY')
if env_key:
    print(f"✓ GOOGLE_API_KEY found in environment: {env_key[:20]}...")
else:
    print("✗ GOOGLE_API_KEY not found in environment")

# Test AIDirector initialization
print("\nInitializing AIDirector...")
try:
    director = AIDirector()
    print("✓ AIDirector initialized successfully")
    print(f"✓ Using model: {director.model_name}")
except Exception as e:
    print(f"✗ Error initializing AIDirector: {e}")

print("=" * 60)
