from midi2jsonAndWavs.main import *
import json
import csv

if __name__ == "__main__":
    obj = Midi2Json("./test.mid")
    obj.read()
    obj.process_lyrics()
    obj.to_wavs()
    print(obj.result)
    # 假设 obj.result 是一个列表，每个元素是列表，输出为csv矩阵
    with open("result.csv", "w", encoding="utf-8", newline='') as f:
        if isinstance(obj.result, list) and obj.result:
            writer = csv.writer(f)
            writer.writerows(obj.result)
        else:
            print("obj.result 不是有效的列表或为空")
