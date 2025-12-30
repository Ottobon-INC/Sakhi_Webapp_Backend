
import os
import uuid
from datetime import datetime
from modules.conversation import save_sakhi_message
from supabase_client import supabase_select

def test_db_integration():
    print("🚀 Starting Database Integration Test...")
    
    # 1. Setup test data
    user_id = str(uuid.uuid4())
    message = "Test message with RAG links"
    lang = "en"
    youtube_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    infographic_url = "https://example.com/test-infographic.png"
    
    print(f"Submitting test message for user: {user_id}")
    
    # 2. Execute save
    try:
        result = save_sakhi_message(user_id, message, lang, youtube_link, infographic_url)
        print("✅ Data submitted to Supabase successfully!")
        print(f"Result: {result}")
        
        # 3. Verify insertion
        print("\n🔍 Verifying insertion...")
        # We need to wait a moment for Supabase to reflect changes if necessary
        # but usually it's immediate for REST API
        
        # Check the database for the inserted row
        # We search by user_id
        check_data = supabase_select(
            "sakhi_conversations",
            filters=f"user_id=eq.{user_id}"
        )
        
        if check_data and len(check_data) > 0:
            row = check_data[0]
            print("✅ Verification Successful! Found row in database:")
            print(f"   - Message: {row.get('message_text')}")
            print(f"   - YouTube Link: {row.get('youtube_link')}")
            print(f"   - Infographic URL: {row.get('infographic_url')}")
            
            if row.get('youtube_link') == youtube_link and row.get('infographic_url') == infographic_url:
                print("\n🎉 INTEGRATION TEST PASSED! The new columns are working correctly.")
            else:
                print("\n❌ INTEGRATION TEST FAILED: Columns were not saved correctly.")
        else:
            print("\n❌ INTEGRATION TEST FAILED: Could not find the inserted row.")
            
    except Exception as e:
        print(f"\n❌ Error during integration test: {e}")
        print("\nDouble check your .env file and ensure the columns have been added to the database.")

if __name__ == "__main__":
    test_db_integration()
