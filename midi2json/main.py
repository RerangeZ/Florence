import mido
import pyttsx3
import os

class Midi2Json:
    def tick_to_seconds(self, tick, tempo=None):
        # tempo: 微秒每拍，默认500000（120BPM）
        if not self.midiFile:
            raise ValueError("请先调用read()方法读取MIDI文件。")
        ticks_per_beat = self.midiFile.ticks_per_beat
        if tempo is None:
            tempo = 500000
        return tick * tempo / ticks_per_beat / 1_000_000
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
                if msg.type == "note_on" or msg.type == "note_off":
                    # 计算音符的开始时间和结束时间
                    # 需要追踪每个音符的起始时间
                    if not hasattr(self, 'note_times'):
                        self.note_times = {}
                        self.current_time = 0
                    self.current_time += msg.time
                    if msg.type == "note_on" and msg.velocity > 0:
                        # 记录音符开始时间
                        self.note_times[msg.note] = self.current_time
                    else:
                        # note_off 或 note_on velocity=0 视为音符结束
                        start_time = self.note_times.get(msg.note, None)
                        if start_time is not None:
                            end_time = self.current_time
                            # 获取tempo（只取第一个tempo事件，适用于大多数流行MIDI）
                            tempo = 500000
                            for t in self.midiFile.tracks:
                                for m in t:
                                    if m.type == 'set_tempo':
                                        tempo = m.tempo
                                        break
                                else:
                                    continue
                                break
                            # 将MIDI音符号转换为频率（Hz）
                            frequency = 440.0 * (2 ** ((msg.note - 69) / 12))
                            start_sec = self.tick_to_seconds(start_time, tempo)
                            end_sec = self.tick_to_seconds(end_time, tempo)
                            self.result[-1].append([
                                frequency,
                                start_sec,
                                end_sec
                            ])
                            del self.note_times[msg.note]
        print("歌词提取完毕。")

    def check_res_file(self):
        if os.path.exists('./res'):
            os.remove("./res")
        os.makedirs('./res')
    
    def to_wavs(self):
        print(f"tts引擎信息：{self.tts_engine.getProperty('voice')}")
        for wordList in self.result:
            word = wordList[0]
            self.tts_engine.save_to_file(word, f"./res/{word}.wav")
        self.tts_engine.runAndWait()

