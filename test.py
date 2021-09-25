import unittest
import api

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

if __name__ == '__main__':
    unittest.main()

