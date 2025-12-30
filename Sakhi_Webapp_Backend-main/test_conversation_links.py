
import sys
import os
from unittest.mock import patch, MagicMock
import unittest

# Add current directory to path to import modules
sys.path.append(os.getcwd())

# Mock environment variables BEFORE importing modules that use them
os.environ["SUPABASE_URL"] = "https://example.supabase.co"
os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "dummy-key"

# Mock the supabase_client module entirely to avoid initialization logic
mock_supabase_client = MagicMock()
sys.modules["supabase_client"] = mock_supabase_client
# We need to make sure supabase_insert is available on the mock
mock_supabase_client.supabase_insert = MagicMock()

# Now import the module under test
from modules.conversation import save_sakhi_message

class TestConversationLinks(unittest.TestCase):
    
    def test_save_sakhi_message_with_links(self):
        # Setup
        user_id = "test-user-123"
        message = "Here is the info"
        lang = "en"
        youtube_link = "https://youtube.com/watch?v=123"
        infographic_url = "https://example.com/info.png"
        
        # Execute
        save_sakhi_message(user_id, message, lang, youtube_link, infographic_url)
        
        # Verify
        mock_supabase_client.supabase_insert.assert_called_once()
        args, _ = mock_supabase_client.supabase_insert.call_args
        table_name = args[0]
        payload = args[1]
        
        self.assertEqual(table_name, "sakhi_conversations")
        self.assertEqual(payload["user_id"], user_id)
        self.assertEqual(payload["message_text"], message)
        self.assertEqual(payload["youtube_link"], youtube_link)
        self.assertEqual(payload["infographic_url"], infographic_url)
        print("✅ Test passed: Links correctly passed to supabase_insert payload.")

if __name__ == '__main__':
    unittest.main()
