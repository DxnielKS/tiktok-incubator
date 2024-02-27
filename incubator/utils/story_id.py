import hashlib

def generate_unique_id(story_content):
    # Use SHA-256 hashing to generate a unique ID for the story content
    return hashlib.sha256(story_content.encode('utf-8')).hexdigest()