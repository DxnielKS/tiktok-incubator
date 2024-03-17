from openai import OpenAI


class Cleaner:

    def __init__(self) -> None:
        pass

    def clean_story(raw_story):
        
        try:
            description_response = openai.chat.completions.create(
            messages=[
                    {"role": "system", "content": "You are hired as a caption-writer for reddit story tiktok videos. Your goal is to make good captions that are funny and related to the story in some way. Limit the caption to about 10-15 words and focus on it being a caption that funnily comments on the story from the point of view of a viewer. Use colloquial langauge like lol, lmao and wth. Use emoji's too."},
                    {"role": "user", "content": f"Make a caption for this reddit story TikTok, you should only return the text that will be used as the caption. {content}."},
                ],
                model="gpt-3.5-turbo",
            )

            description = f"{description_response.choices[0].message.content} {hashtags}"

            _LOGGER.info(f'Caption {description}')

        except Exception as e:
            console.print(e)
            description = f"Dayum 😳 {hashtags}"

        return raw_story