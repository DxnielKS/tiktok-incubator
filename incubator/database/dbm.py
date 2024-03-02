from incubator.utils.story_id import generate_unique_id
from incubator.utils.di import inject_supabase_client
import uuid
import datetime
import logging

_LOGGER = logging.getLogger('incubator.database')


def check_if_story_posted(story, supabase_client=inject_supabase_client()) -> bool:
    hashed = generate_unique_id(story)
    data = supabase_client.table('videos_posted').select("*").eq('video_hash', hashed).execute()
    return len(data.data) > 0


def log_story_posted(title, story, supabase_client=inject_supabase_client()) -> bool:
    hashed = generate_unique_id(story)
    try:
        supabase_client.table('videos_posted').insert({
            "id": str(uuid.uuid4()),
            "video_hash": hashed,
            "title": title,
            'story': story,
            'created_at': datetime.datetime.utcnow().isoformat()
        }).execute()
    except Exception as e:
        _LOGGER.error(f'Error logging video upload {e}')
        return False
    return True