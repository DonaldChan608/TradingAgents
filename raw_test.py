#!/usr/bin/env python3
"""
Raw HTTP test to see exactly what OpenRouter returns
"""

import os
import requests
import json

def test_openrouter_raw():
    """Test OpenRouter API with raw HTTP requests"""
    print("🔍 TESTING OPENROUTER API WITH RAW HTTP REQUESTS")
    print("=" * 60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No API key found!")
        return
    
    # Test with raw requests
    url = "https://openrouter.ai/api/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/TradingAgents",
        "X-Title": "TradingAgents"
    }
    
    data = {
        "model": "text-embedding-3-small",
        "input": "High inflation rate with rising interest rates and declining consumer spending"
    }
    
    print(f"Making request to: {url}")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Data: {json.dumps(data, indent=2)}")
    print("-" * 40)
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response content type: {response.headers.get('content-type', 'unknown')}")
        print(f"Response length: {len(response.text)} characters")
        
        print(f"\n🔍 RESPONSE CONTENT ANALYSIS:")
        print(f"First 1000 characters: {response.text[:1000]}")
        
        if len(response.text) > 1000:
            print(f"Last 1000 characters: {response.text[-1000:]}")
        
        # Analyze the content
        if response.text.strip().startswith('<!DOCTYPE') or response.text.strip().startswith('<html'):
            print("\n🚨 CRITICAL ISSUE: OpenRouter is returning an HTML web page!")
            print("This explains why the OpenAI client fails - it expects JSON, not HTML")
            print("OpenRouter is serving their website instead of the API endpoint")
            
            # Look for clues in the HTML
            if "openrouter" in response.text.lower():
                print("✅ HTML contains 'openrouter' - confirms this is their website")
            if "api" in response.text.lower():
                print("ℹ️ HTML mentions 'api' - might be a redirect or error page")
            if "error" in response.text.lower():
                print("⚠️ HTML contains 'error' - might be an error page")
                
        elif response.text.strip().startswith('{') or response.text.strip().startswith('['):
            print("\n📄 This appears to be JSON data")
            try:
                json_response = json.loads(response.text)
                print(f"✅ JSON parsed successfully!")
                print(f"JSON keys: {list(json_response.keys()) if isinstance(json_response, dict) else 'Array'}")
                print(f"Full JSON: {json.dumps(json_response, indent=2)}")
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing failed: {e}")
                print("This suggests malformed JSON from OpenRouter")
        else:
            print("\n❓ Unknown content format")
            print("This suggests a serious issue with OpenRouter's API")
        
        # Check if it's an error response
        if response.status_code != 200:
            print(f"\n⚠️ Non-200 status code: {response.status_code}")
            print("This suggests an API error or authentication issue")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        print(f"Error type: {type(e)}")

if __name__ == "__main__":
    test_openrouter_raw()

