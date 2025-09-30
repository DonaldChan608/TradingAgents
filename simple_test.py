#!/usr/bin/env python3
"""
Very simple test to isolate the AttributeError and see what OpenRouter returns
"""

import os
import logging
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_openrouter_direct():
    """Test OpenRouter API directly to see what it returns"""
    print("🔍 TESTING OPENROUTER API DIRECTLY")
    print("=" * 60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No API key found!")
        return
    
    try:
        # Create client
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        print("✅ OpenAI client created successfully")
        print(f"Backend URL: {client.base_url}")
        
        # Test text
        test_text = "High inflation rate with rising interest rates and declining consumer spending"
        print(f"\n📋 Testing with text: {test_text[:50]}...")
        
        # Make the API call
        print("🔄 Making API call...")
        response = client.embeddings.create(
            model="text-embedding-3-small", 
            input=test_text
        )
        
        print("✅ API call completed!")
        print(f"Response type: {type(response)}")
        print(f"Response class: {response.__class__.__name__}")
        
        # Now let's see what's in the response
        print(f"\n🔍 RESPONSE ANALYSIS:")
        print(f"Response has 'data' attribute: {hasattr(response, 'data')}")
        
        if hasattr(response, 'data'):
            print(f"Data type: {type(response.data)}")
            print(f"Data length: {len(response.data) if response.data else 'None'}")
            
            if response.data and len(response.data) > 0:
                first_item = response.data[0]
                print(f"First item type: {type(first_item)}")
                print(f"First item has 'embedding' attribute: {hasattr(first_item, 'embedding')}")
                
                if hasattr(first_item, 'embedding'):
                    embedding = first_item.embedding
                    print(f"✅ Embedding retrieved successfully!")
                    print(f"Embedding type: {type(embedding)}")
                    print(f"Embedding length: {len(embedding)}")
                    print(f"First few values: {embedding[:5]}")
                else:
                    print(f"❌ First item missing 'embedding' attribute")
                    print(f"Available attributes: {[attr for attr in dir(first_item) if not attr.startswith('_')]}")
            else:
                print("❌ Data array is empty")
        else:
            print("❌ Response missing 'data' attribute")
            print(f"Available attributes: {[attr for attr in dir(response) if not attr.startswith('_')]}")
            
            # Try to see what the response actually contains
            if hasattr(response, '__str__'):
                response_str = str(response)
                print(f"\n🔍 RESPONSE CONTENT:")
                print(f"String length: {len(response_str)} characters")
                print(f"First 1000 characters: {response_str[:1000]}")
                if len(response_str) > 1000:
                    print(f"Last 1000 characters: {response_str[-1000:]}")
                
                # Analyze content
                if response_str.strip().startswith('<!DOCTYPE') or response_str.strip().startswith('<html'):
                    print("🚨 This is an HTML web page, not API data!")
                elif response_str.strip().startswith('{') or response_str.strip().startswith('['):
                    print("📄 This appears to be JSON data but was returned as a string")
                else:
                    print("❓ Unknown content format")
        
    except Exception as e:
        print(f"❌ API call failed!")
        print(f"Error type: {type(e)}")
        print(f"Error class: {e.__class__.__name__}")
        print(f"Error message: {str(e)}")
        
        # Check if error has response info
        if hasattr(e, '__dict__'):
            print(f"Error attributes: {list(e.__dict__.keys())}")

if __name__ == "__main__":
    test_openrouter_direct()

