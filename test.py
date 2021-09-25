import unittest
import api
import os
import shutil

class TestPrivateMethods(unittest.TestCase):

    def test__all_videos(self):
        path = '/media'
        r = api._all_videos(path)
        self.assertEqual(len(r), 61) # 61 videos
        self.assertEqual(r[0][0], '/media/yui_aragaki_compilation-Scene-001.mp4') # first one
        self.assertEqual(r[-1][0], '/media/yui_aragaki_compilation-Scene-155.mp4') # second one

    def test__thumb_path(self):
        path = '/media/yui_aragaki_compilation-Scene-001.mp4'
        r = api._thumb_path(path)
        self.assertEqual(r, '/media/.thumb/yui_aragaki_compilation-Scene-001.png')

    def test__get_all_data(self):
        r = api._get_all_data()
        self.assertEqual(len(r['videos']), 61) # 61 videos
        self.assertEqual(r['videos'][0]['video_name'], 'yui_aragaki_compilation-Scene-155') # first one
        self.assertEqual(r['videos'][0]['video_path'], '/media/yui_aragaki_compilation-Scene-155.mp4')
        self.assertEqual(r['videos'][0]['thumb_path'], '/media/.thumb/yui_aragaki_compilation-Scene-155.png')
    
    def test__get_thumbnail_status(self):
        orphaned, uncreated = api._get_thumbnail_status()
        self.assertEqual(len(orphaned), 0)
        self.assertEqual(len(uncreated), 0)
        # Add another vid
        r = api._get_all_data()
        src = r['videos'][0]['video_path']
        dst1 = '/media/tmp1.mp4'
        shutil.copyfile(src, dst1)
        dst2 = '/media/tmp2.mp4'
        shutil.copyfile(src, dst2)
        #
        r = api._get_all_data()
        self.assertEqual(len(r['videos']), 63)
        _, uncreated = api._get_thumbnail_status()
        self.assertEqual(len(uncreated), 2)
        self.assertEqual(uncreated[0][0:3], 'tmp') # make sure the name is correct
        # create thumbs
        api._create_thumbs_for(uncreated)
        _, uncreated = api._get_thumbnail_status()
        self.assertEqual(len(uncreated), 0) # thumbnails should have been created
        # create orphans
        orphans, _ = api._get_thumbnail_status()
        self.assertEqual(len(orphans), 0)
        os.remove(dst1)
        os.remove(dst2)
        orphans, _ = api._get_thumbnail_status()
        self.assertEqual(len(orphans), 2)
        # clean up unused thumbs
        api._cleanup_thumbs_for(orphans)
        orphans, uncreated = api._get_thumbnail_status()
        self.assertEqual(len(orphans), 0)
        self.assertEqual(len(uncreated), 0)



if __name__ == '__main__':
    unittest.main()

