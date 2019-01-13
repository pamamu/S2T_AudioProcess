import Pyro4

from ContainerHandler import ContainerHandler
from src.Audio import Audio


@Pyro4.expose
class AudioProcessHandler(ContainerHandler):

    def __init__(self, container_name, main_uri):
        super().__init__(container_name, main_uri)

    def run(self, **kwargs):
        if 'input_json' in kwargs and 'output_folder' in kwargs:
            print("Container {}: Runned with {}".format(self.container_name, kwargs))
            self.running = True
            result = self.process_audio(kwargs['input_json'], kwargs['output_folder'])
            self.running = False
            return result
        else:
            raise TypeError('input_json and output_folder required')
        pass

    def info(self):
        pass

    def process_audio(self, input_data, output_folder):
        audio = Audio(data=input_data, output_folder=output_folder)
        print("BEGIN")
        audio.check_up()
        print("\tPREPROCESADO")
        audio.clean_audio()
        print("\tAUDIO LIMPIO")
        audio.split_audio()
        print("\tAUDIO SPLITTED")
        return audio.process_output()
