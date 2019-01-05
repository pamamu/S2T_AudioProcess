import json

from src.Audio import Audio


class AudioProcessHandler:
    def __init__(self, config):
        self.start(config)

    def start(self, config):
        audio = Audio(data=config)
        print("BEGIN")
        audio.check_up()
        print("\tPREPROCESADO")
        audio.clean_audio()
        print("\tAUDIO LIMPIO")
        audio.split_audio()
        print("\tAUDIO SPLITTED")
        audio.process_output()


if __name__ == '__main__':
    input_data = json.loads(open('src/json_examples/input_example.json').read())
    if type(input_data) is list:
        for i in input_data:
            handler = AudioProcessHandler(i)
    else:
        handler = AudioProcessHandler(input_data)
