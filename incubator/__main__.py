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

    if not os.path.exists("temp-assets"):
        os.mkdir("temp-assets")

    video_background_file = "raw-videos/background.mp4"  # Your video background file
    video_background_offset = random.randint(0, 5000)  # Starting Position of Video : 0 for Beginning
    image_banner_file = "OIP.jpg"  # Your image banner file
    output_file = "final-videos/video.mp4"  # The output filename

    content = """I (26 F) have a pretty close group of friends.
    We have this one girl in our group, Sadie (27 F).
    She has a disability that is mostly manageable through medication.
    Despite this, Sadie has a bad habit of ‘forgetting’ to take her pills right before we do something she isn’t interested in doing.
    This time, it was on a group trip we’ve been planning for over a year.
    Due to how high the cost of the trip was, we each decided to take a day and plan an activity that the whole group would participate in.
    We also rented a van together to get to our destination as that was the most ideal situation.
    The first issue with Sadie came up when getting to our destination.
    Due to the length of the drive, everyone was going to be driving an hour to get to our destination.
    Right before it was Sadie’s turn, she had a flare up, and could not drive. Our friend took over.
    The next morning, my friend had planned a tour of the town.
    We all reminded Sadie several times to take her medication as this was an expensive tour and we did not want it to be cut short.
    Well, she had forgotten and the tour had to be cut short.
    This is when I got genuinely upset because this was now my money being wasted.
    Throughout the week, she had flare ups pretty often.The actual fight that led to this post occurred on my day though.
    The previous day, Sadie had had no flare ups. (It was also her day to plan).
    This was because she had set alarms to take her medication regularly so that she would be ok.
    We all reminded her to please take her pills like that again.
    I decided to take all my friends on a trail ride on horses as the trails in this town are known for being absolutely beautiful.
    We paid extra for a basics lesson prior to the trail.
    In the basics lesson, we were all paired off based on experience and performance in the small arena that they had.
    I was paired with Sadie.
    Well, 1/4th of the way through the trail, she started having a flare up.
    I told her that I would not be turning around as this was expensive and that I was truly looking forward to this.
    She begged me to turn around. Finally, the ranger told us that I had to turn around with her as she was my partner.
    In the car, I told her that she knew how important this was to me and that she just should’ve taken the pills.
    She told me that I was being ableist and that I didn’t know what the pills did to her.
    We got into a huge argument in which I said “if your disability can’t take being a good friend, then maybe you shouldn’t come on these trips anyway.”
    While I agree that it was harsh, I didn’t think I was in the wrong considering that she had cost us so much money over the years for simply not wanting to do something.
    My other friends agree that Sadie is inconvenient at times but that I should’ve been more sensitive to her condition.
    I’m honestly torn on whether to apologize or not."""

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
