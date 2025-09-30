#!/usr/bin/env python3
"""
Test script to see the enhanced logging and capture what OpenRouter is actually returning
"""

import os
import sys
import logging

# Add the tradingagents directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'tradingagents'))

from agents.utils.memory import FinancialSituationMemory

def test_enhanced_logging():
    """Test the enhanced logging to see what OpenRouter returns"""
    print("🔍 TESTING ENHANCED LOGGING TO SEE OPENROUTER RESPONSE")
    print("=" * 60)
    
    # Set up detailed logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create a test configuration
    test_config = {
        "backend_url": "https://openrouter.ai/api/v1",
        "project_dir": ".",
        "results_dir": "./results"
    }
    
    try:
        # Initialize memory system
        print("📋 Initializing memory system...")
        memory = FinancialSituationMemory("test_memory", test_config)
        
        # Test text for embedding
        test_text = "High inflation rate with rising interest rates and declining consumer spending"
        print(f"\n📋 Testing embedding generation for text: {test_text[:50]}...")
        print("This should trigger the enhanced logging to show what OpenRouter returns...")
        
        # This should fail with OpenRouter and show detailed logging
        embedding = memory.get_embedding(test_text)
        
        print(f"\n✅ Embedding generated successfully!")
        print(f"   Embedding type: {type(embedding)}")
        print(f"   Embedding length: {len(embedding)}")
        
    except Exception as e:
        print(f"\n❌ Test completed with exception: {e}")
        print(f"Check the logs above to see what OpenRouter actually returned!")

if __name__ == "__main__":
    test_enhanced_logging()
