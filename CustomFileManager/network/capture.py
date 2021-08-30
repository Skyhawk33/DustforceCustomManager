from time import sleep
from scapy.layers.http import *
from scapy.layers.l2 import Ether
from scapy.sendrecv import AsyncSniffer


class SubmissionReader:
    def __init__(self):
        self._multipart_data = b''
        self._reading = False
        self._sniffer = AsyncSniffer(store=0, prn=self._pkt_callback, lfilter=lambda x: x.haslayer(TCP))
        self.last_replay = None
        self.replay_callback = None
        self.active = False

    def _build_replay_data(self):
        replay_data = {}
        try:
            for token in str(self._multipart_data).split('name="'):
                if "'" in token:
                    continue
                key, rest = token.split('"\\r\\n\\r\\n', 1)
                data, _ = rest.split('\\r\\n-', 1)
                replay_data[key] = data
        except ValueError:
            print('ERROR PARSING REPLAY DATA')
            for token in str(self._multipart_data).split('name="'):
                print(token)

        if 'extra' in replay_data:
            extra_data = replay_data['extra']
            del replay_data['extra']
            for token in extra_data.split('&'):
                key, data = token.split('=')
                replay_data[key] = data
        return replay_data

    def _pkt_callback(self, pkt):
        # if pkt[HTTP].Path == b'/backend8/add_score.php':
        #     print('Score submission')
        if pkt.haslayer(HTTPRequest) and pkt[HTTP].Path == b'/backend8/add_score.php':
            self._multipart_data = bytes(pkt[HTTP].Content_Type)
            self._reading = True
        elif self._reading and 'Content-Disposition: form-data' in str(pkt):
            while pkt.payload:
                pkt = pkt.payload
            self._multipart_data += pkt.load
            if all(key in self._multipart_data for key in (b'user', b'level', b'score1', b'score2')):
                replay_data = self._build_replay_data()
                self._multipart_data = b''
                self._reading = False
                if self.replay_callback:
                    self.replay_callback(replay_data)
                self.last_replay = replay_data

    def set_callback(self, callback):
        self.replay_callback = callback

    def start(self):
        self._sniffer.start()
        self.active = True

    def stop(self):
        self._sniffer.stop(join=True)
        self.active = False


if __name__ == '__main__':
    def test_callback(replay):
        print(replay)


    capture = SubmissionReader()
    capture.set_callback(test_callback)
    capture.start()
    sleep(5)
    capture.stop()
    sleep(1)
    capture.start()
    sleep(50)
    capture.stop()
