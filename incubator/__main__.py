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

    content = """The story of my red penis is a tale of mystery and adventure,
    a quest filled with juvenile confusion and dangerously high levels of awkwardness.
    In the winter after I turned 21, I started to find dead skin on my underwear.
    Every day I would notice more and more accumulating there, along with increasing itchiness in the area of my perineum where that skin was coming from.
    Since the region was not visible to my eye, I never noticed the patch of red, irritated skin I had there, but after putting up with the discomfort for a while I figured it was time to do something about it. I pluck up the courage and, with this symptom under my belt, went to my first doctor ready to face the awkwardness.
    Because the problem was located in the genital area, I figured the right doctor to see was a urologist.
    I felt a bit anxious coming to the appointment. I guess most people wouldn’t be thrilled by the idea of having their genitals examined either,
    but bear in mind that, back then, I was a 21-year-old virgin with no sexual experience whatsoever. My penis had remained concealed for many years,
    kept secret like the Ark of the Covenant waiting for an Indiana Jones to discover it. I had always pictured someone a bit different to show my penis to for the first time,
    but I guess a short-winded, 60-year-old doctor with tired analytical eyes and a shaky hand would have to do.
    He asked me to drop my pants and lie down, and instructed me to move my penis right and left like a joystick,
    then my testicles, in order to expose the whole affected area.
    As I stood back up, pulling up my pants, my face still red from the embarrassment,
    he passed a disappointing sentence.
    “This is a skin problem, I can’t really help you with that. You should see a dermatologist”. Like a teenage girl with daddy issues, I had given away my flower to the wrong guy. That same evening I looked for a dermatologist and made the second of a large list of doctor appointments.
    My first visit to the dermatologist came a few days later.
    The fact that it was the second time going through such a process made it only slightly less awkward.
    He prescribed some lotions for me and scheduled a second visit the following week.
    The lotions didn’t do anything, so on my second visit he took another look at it and wrote me a prescription for a new lotion.
    Seven days later my skin is the same, and I’m walking to my third appointment with this guy wondering whether he is really just a creep that’s writing me prescriptions for placebo to get to see my dick every week.
    So I’m there, pants down, exposing my privates once again,
    and this time the doctor notices a new patch of dry skin a bit further up,
    on the base of my penis.
    He takes a sample of the skin there to get it sent to the laboratory, and it turns out to be a genital wart."""

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
