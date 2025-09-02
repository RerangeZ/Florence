import mido

class Midi2Json:
    midiPath:str
    midiFile:mido.MidiFile |None
    track: mido.MidiTrack
    result:list[list]
    def __init__(self, path) -> None:
        self.midiPath = path
        self.midiFile = None
        self.result = []
    def read(self):
        self.midiFile = mido.MidiFile(self.midiPath)
        self.track = self.midiFile.tracks[0]
        return

    def process_lyrics(self):
        if not self.midiFile:
            print("请先调用read()方法读取MIDI文件。")
            return
        for i, track in enumerate(self.midiFile.tracks):
            print(f"Track {i}:")
            for msg in track:
                if msg.type in ("lyrics", "lyric"):
                    text = msg.text.encode('latin1').decode('utf-8')
                    print(text)
                    self.result.append([text])
        print("歌词提取完毕。")

