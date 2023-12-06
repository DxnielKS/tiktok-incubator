from incubator.clipper import *
from tiktok_uploader.upload import upload_video, upload_videos
from tiktok_uploader.auth import AuthBackend
import tiktok_uploader
import os

# line of code to make the upload page work.. for some reason the package uses a funky upload page url
tiktok_uploader.config['paths']['upload'] = 'https://www.tiktok.com/upload?lang=en'

def upload_local_video(video_name):
    """Function to take in a video stored locally and upload to tiktok using the cookies stored locally."""
    upload_video(f'final-videos/{video_name}',
                 description='this is my description',
                 cookies='cookies.txt'
                 )

def main():

    # TURN RAW CLIPS INTO FINAL VIDEO
    console = Console()
    banner = pyfiglet.figlet_format(text='AutoClip', font='rectangles')
    console.print()
    console.print("[bold][red1]" + banner)
    console.print("[dark_red] By Abhishta (github.com/abhishtagatya)")

    if not os.path.exists("temp_assets"):
        os.mkdir("temp_assets")

    video_background_file = "raw-videos/background.mp4"  # Your video background file
    video_background_offset = random.randint(0, 5000)  # Starting Position of Video : 0 for Beginning
    image_banner_file = "OIP.jpg"  # Your image banner file
    output_file = "final-videos/video.mp4"  # The output filename

    content = """Taniel woke up feeling unusually anxious.
            Today was his long-awaited doctor's appointment.
            He had always been nervous about medical visits.
            As he sat in the waiting room, his mind raced with possibilities.
            "What if it's something serious?" he thought.
            Finally, his name was called, and he walked in.
            The doctor, a kind-faced woman, greeted him warmly.
            She asked routine questions, making notes on her clipboard.
            Taniel tried to answer calmly, but his voice betrayed his nervousness.
            The doctor noticed and reassured him with a smile.
            After a thorough check-up, she told him he was in perfect health.
            Relief washed over Taniel like a wave.
            He thanked the doctor and left the clinic feeling lighter.
            On his way home, Taniel couldn't help but laugh at his earlier fears.
            He decided to share his story on Reddit, where it was met with a mix of sympathy and amusement.
            Taniel's tale became a reminder to not let anxiety overshadow reality."""

    console.print("\n\n[light_green] Task Starting\n\n")
    clip(content=content,
         video_file=video_background_file,
         image_file=image_banner_file,
         outfile=output_file,
         offset=video_background_offset)

    console.print("\n\n[light_green] Completed!")

    # UPLOAD FINAL VIDEO TO TIKTOK
    upload_local_video('video.mp4')


if __name__ == "__main__":
    main()
