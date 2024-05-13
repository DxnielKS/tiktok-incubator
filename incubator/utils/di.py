from functools import wraps
import os
from supabase import create_client
from dotenv import load_dotenv
load_dotenv(())

def inject_supabase_client():
    api_url = os.getenv('SUPABASE_URL')
    api_key = os.getenv('SUPABASE_KEY')
    supabase_client = create_client(api_url, api_key)
    return supabase_client

