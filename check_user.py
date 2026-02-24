
from supabase_client import supabase

def list_users():
    try:
        response = supabase.table("users").select("email").limit(5).execute()
        if response.data:
            print(f"Users found: {response.data}")
        else:
            print("No users found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_users()
