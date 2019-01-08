import json
import socket

from src.Audio import Audio
import Pyro4


@Pyro4.expose
class AudioProcessHandler:

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

    def hello(self):
        print("hello")
        return "hello"


def getIp():
    """
    TODO DOCUMENTATION
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


if __name__ == '__main__':
    handler = AudioProcessHandler()
    daemon = Pyro4.Daemon(host=getIp(), port=4040)
    uri = daemon.register(handler, objectId="AudioProcess")
    print(uri)
    daemon.requestLoop()

# input_data = json.loads(open('src/json_examples/input_example.json').read())
# if type(input_data) is list:
#     for i in input_data:
#         handler = AudioProcessHandler(i)
# else:
#     handler = AudioProcessHandler(input_data)
