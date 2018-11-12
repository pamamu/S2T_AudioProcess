from Audio import Audio
import json

class AudioProcessHandler:
    def __init__(self, config):
        self.start(config)

    def start(self, config):
        audio = Audio(data=config)
        audio.check_up()
        audio.clean_audio()
        audio.split_audio()
        audio.process_output()


if __name__ == '__main__':
    handler = AudioProcessHandler(json.loads(open('src/json_examples/input_example.json').read()))
