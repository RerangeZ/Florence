import mido
import pyttsx3

class Midi2Json:
    midiPath:str
    midiFile:mido.MidiFile |None
    track: mido.MidiTrack
    result:list[list]
    tts_engine:pyttsx3.Engine
    def __init__(self, path) -> None:
        self.midiPath = path
        self.midiFile = None
        self.result = []
        self.tts_engine = pyttsx3.init()
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
    
    def to_wavs(self):
        print(f"tts引擎信息：{self.tts_engine.getProperty('voice')}")
        for wordList in self.result:
            word = wordList[0]
            self.tts_engine.save_to_file(word,f"./res/{word}.wav")
            self.tts_engine.runAndWait()

