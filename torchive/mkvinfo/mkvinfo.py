from enzyme import MKV
from models import VideoTrack, AudioTrack, SubTrack


class Mkvinfo:
    def __init__(self, filename):
        with open(filename) as f:
            self.mkv = MKV(f)
            self.title = self.mkv.info.title
            self.duration = self.mkv.info.duration

    @property
    def video_tracks(self):
        return [VideoTrack(track) for track in self.mkv.video_tracks]

    @property
    def audio_tracks(self):
        return [AudioTrack(track) for track in self.mkv.audio_tracks]

    @property
    def sub_tracks(self):
        return [SubTrack(track) for track in self.mkv.subtitle_tracks]

    @property
    def all(self):
        return {
            'title': self.title,
            'duration': self.duration.total_seconds(),
            'tracks': {
                'video': [track.json() for track in self.video_tracks],
                'audio': [track.json() for track in self.audio_tracks],
                'sub': [track.json() for track in self.sub_tracks]
            }
        }

    @property
    def all_json(self):
        return {
            'title': self.title,
            'duration': self.duration.total_seconds(),
            'video': [track.json() for track in self.video_tracks],
            'audio': [track.json() for track in self.audio_tracks],
            'subs': [track.json() for track in self.sub_tracks]
        }


