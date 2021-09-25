import os
import glob
import json
import datetime
from flask import Flask, render_template, redirect, url_for, send_from_directory
from pathlib import Path
from thumbnail import create_thumb, name_list

base_path = "/media"
thumb_path = os.path.join(base_path, ".thumb")
Path(thumb_path).mkdir(parents=True, exist_ok=True)

app = Flask(__name__)

def _all_videos(dir_path):
    """ Get all video files from a given path, sorted by created time, decending
    """
    all_files = list(filter(os.path.isfile, glob.glob(os.path.join(dir_path, "*.mp4"))))
    all_files = [(x, os.path.getctime(x)) for x in all_files]
    return all_files

def _thumb_path(file_path, thumb_path='.thumb', img_ext='png'):
    """ Return the thumbnail path of a given path
    """
    parts = file_path.split('/')
    parts.insert(len(parts)-1, thumb_path)
    parts[len(parts)-1] = parts[-1].replace('mp4', img_ext)
    return '/'.join(parts)

def _get_all_data():
    """ Return the full list of video files
    """
    data = []
    all_vids = _all_videos(base_path)
    all_vids.sort(key=lambda x:x[1], reverse=True)

    for a in all_vids:
        d = {
            'video_name': a[0].split('/')[-1].replace('.mp4', ''),
            'video_path': a[0],
            'thumb_path': _thumb_path(a[0]),
            'created_time': str(datetime.datetime.fromtimestamp(a[1]))
            }
        data.append(d)
    return {'videos': data}

@app.route('/')
def list_files():
    data = _get_all_data()
    return render_template('index.html', data=data)

@app.route('/list')
def list_files_api():
    data = _get_all_data()
    return data

@app.route('/refresh_thumbs/<video_path>')
def refresh_thumbs(video_path):
    create_thumb(video_path)
    return 'updated thumbnail for %s' % video_path

@app.route('/delete/<video_name>')
def delete(video_name):
    fn = f'{base_path}{video_name}.mp4'
    os.remove(fn)
    return redirect('/')

@app.route('/refresh_all_thumbs')
def refresh_all_thumbs():
    #thumb_path = f"{base_path}.thumb/"
    # Get just the base names of the files
    vids = name_list(base_path, 'mp4')
    thumbs = name_list(thumb_path, 'png')

    # find a list of orphaned thumbs and remove them
    for o in thumbs - vids:
        fn = f'{thumb_path}{o}.png'
        print('removing', fn)
        os.remove(fn)

    #find a list of un-thumbed videos and create thumbnails
    for v in vids - thumbs:
        fn = os.path.join(base_path, f"{v}.mp4")
        print('creating', fn)
        create_thumb(fn)

    return redirect('/')

@app.route('/media/<path:path>')
def send_media(path):
    print(path)
    return send_from_directory(base_path, path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)

