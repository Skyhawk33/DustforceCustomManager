from time import sleep
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class SplitsReader(PatternMatchingEventHandler):
    patterns = ['*/split.txt']

    def __init__(self, folder):
        super(SplitsReader, self).__init__()
        self.last_replay = None
        self.replay_callback = None
        self.active = False
        self._folder = folder
        self._observer = None

    def on_modified(self, event):
        replay_data = self._build_replay_data()
        if self.replay_callback and self.last_replay != replay_data:
            self.replay_callback(replay_data)
        self.last_replay = replay_data

    def _build_replay_data(self):
        # file format:
        # split-id
        # level-id combo-drops completion% milliseconds
        replay_data = {}
        with open(self._folder + "/split.txt", 'r') as f:
            replay_data['id'] = f.readline().strip('\r\n ')
            data = f.readline().strip('\r\n ').split(' ')
        replay_data['level'] = data[0]
        replay_data['score2'] = str(max(5 - int(data[1]), 1))
        replay_data['score1'] = str(max((int(float(data[2])) - 50) // 10, 1))
        replay_data['time'] = data[3]
        return replay_data

    def set_callback(self, callback):
        self.replay_callback = callback

    def start(self):
        if self._observer is not None:
            self.stop()
        self._observer = Observer()
        self._observer.schedule(self, path=self._folder)
        self._observer.start()
        self.active = True

    def stop(self):
        if self._observer is not None:
            self._observer.stop()
            self._observer.join()
        self._observer = None
        self.active = False


if __name__ == '__main__':
    def test_callback(replay):
        print(replay)

    capture = SplitsReader(r'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/')
    capture.set_callback(test_callback)
    capture.start()
    sleep(50)
    capture.stop()
    sleep(1)
    capture.start()
    sleep(50)
    capture.stop()
