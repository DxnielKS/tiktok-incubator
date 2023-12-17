from incubator.clipper import *
from tiktok_uploader.upload import upload_video, upload_videos
from tiktok_uploader.auth import AuthBackend
import tiktok_uploader
import os

# line of code to make the upload page work.. for some reason the package uses a funky upload page url
tiktok_uploader.config['paths']['upload'] = 'https://www.tiktok.com/upload?lang=en'


def upload_local_video(video_name, description, cookies='cookies.txt'):
    """Function to take in a video stored locally and upload to TikTok using the cookies stored locally."""
    upload_video(f'final-videos/{video_name}',
                 description=description,
                 cookies=cookies
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

    content = """Dated a girl for a short period that clearly had trust issues.
    Every time she came to my place the first thing she would do as soon as I went to the restroom was check my browser history on my PC.
    If I had a trace of porn or even looked at a Facebook profile of another female it was all out war.
    Finally had enough.
    She didn't drive so my dumb ass had to drive home this psycho after breaking up with her.
    She was kicking and screaming the entire drive.
    She tried to jump out of the car multiple times while going 65.
    About a month after that I was seeing a new girl in St Louis. Drove down to see her multiple times.
    One of my drives home the psycho ex kept calling and texting.
    She somehow found out I was with a new girl (had her blocked on everything I could think of).
    She sent threatening texts and then sent nudes and kept leaving voice messages just screaming obscenities and messages telling me she was pregnant.
    My service provider at the time didn't allow me to block numbers for some reason so I switched providers and got a new number."""

    console.print("\n\n[light_green] Task Starting\n\n")
    clip(content=content,
         video_file=video_background_file,
         image_file=image_banner_file,
         outfile=output_file,
         offset=video_background_offset)

    console.print("\n\n[light_green] Completed!")

    # UPLOAD FINAL VIDEO TO TIKTOK
    upload_local_video('video.mp4', 'bruh #fyp #tiktok #foryoupage #cartelclips #reddit #askreddit #redditstories #minecraftparkour')


if __name__ == "__main__":
    main()
