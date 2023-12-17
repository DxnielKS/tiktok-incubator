import os

if not os.path.exists('final-videos'):
    os.mkdir('final-videos')
    raise Exception('Need to have a folder named final-videos!')

if not os.path.exists('raw-videos'):
    os.mkdir('raw-videos')
    raise Exception('Need to have folder named raw-videos!')


if not os.path.exists('story-lines'):
    os.mkdir('story-lines')