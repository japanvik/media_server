import imageio
from PIL import Image

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
