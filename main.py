from midi2json.main import *
import json

if __name__ == "__main__":
    obj = Midi2Json("./test.mid")
    obj.read()
    obj.process_lyrics()
    obj.to_wavs()
    print(obj.result)
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(obj.result, f, ensure_ascii=False, indent=2)