from midi2json.main import *

if __name__ == "__main__":
    obj = Midi2Json("./test.mid")
    obj.read()
    obj.process_lyrics()
    obj.to_wavs()
    print(obj.result)