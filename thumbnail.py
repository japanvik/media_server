import imageio
import glob
import os
from PIL import Image

def name_list(path, ext='mp4'):
    """ Return a list of file base names (without extensions) given a path
    """
    l = glob.glob(os.path.join(path, f"*.{ext}"))
    l = [x.split('/')[-1].replace(f'.{ext}', '') for x in l]
    return set(l)

def create_thumb(video_path):
    vid = imageio.get_reader(video_path)
    fps = vid.get_meta_data()['fps']
    ttl = vid.get_meta_data()['duration'] * fps #TTL frames
    # get the middle frame
    frame = vid.get_data(int(ttl/2))
    im = Image.fromarray(frame)
    im = im.resize((192,168))
    # create the thumbnail path
    fn = video_path.split('/')[-1]
    im_path = video_path.replace(fn, f".thumb/{fn.replace('.mp4','.png')}")
    #save the image
    im.save(im_path)
    return im_path

