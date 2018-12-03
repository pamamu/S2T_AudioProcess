"""
TODO DOCUMENTATION
"""

from utils.IO import check_audio_file, get_tmp_folder
from utils.audio_tools import convert_audio, get_working_format
import json
from os import path


class Audio:

    def __init__(self,
                 audio_path=None,
                 samplerate=None,
                 n_channels=None,
                 bitdepth=None,
                 output_format=None,
                 data=None):

        required_params = ['audio_path',
                           'samplerate',
                           'n_channels',
                           'bitdepth',
                           'output_format']
        pre = ""
        if bool(data):
            for key, value in data.items():
                setattr(self, key, value)
            pre = "self."
        for param in required_params:
            if eval(pre + param) is None:
                raise ValueError("Invalid {}".format(param))

        if pre == "":
            self.audio_path = audio_path
            self.samplerate = samplerate
            self.n_channels = n_channels
            self.bitdepth = bitdepth
            self.output_format = output_format

    def check_up(self):
        """
        TODO DOCUMENTATION
        :return:
        """
        check_audio_file(self.audio_path)
        audio_name = path.basename(self.audio_path).split('.')[0]
        audio_conv_path = convert_audio(self.audio_path,
                                        path.join(get_tmp_folder(), audio_name),
                                        self.samplerate,
                                        self.n_channels,
                                        self.bitdepth,
                                        get_working_format())
        print(audio_conv_path)

    def clean_audio(self):
        """
        TODO DOCUMENTATION
        :return:
        """
        print("LIMPIAR AUDIO")
        pass

    def split_audio(self):
        """
        TODO DOCUMENTATION
        :return:
        """
        print("SEPARAR AUDIO")
        pass

    def process_output(self):
        """
        TODO DOCUMENTATION
        :return:
        """
        print("PROCESAR SALIDA")
        pass
