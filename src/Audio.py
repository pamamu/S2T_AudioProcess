"""
TODO DOCUMENTATION
"""

from utils.IO import check_audio_file, get_tmp_folder, clean_tmp_folder
from utils.audio_tools import convert_audio, get_working_format, apply_filters, normalize_audio, noise_removal
import json
from os import path


class Audio:

    def __init__(self,
                 audio_path=None,
                 output_samplerate=None,
                 output_n_channels=None,
                 output_bitdepth=None,
                 output_format=None,
                 data=None):

        required_params = ['audio_path',
                           'output_samplerate',
                           'output_n_channels',
                           'output_bitdepth',
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
            self.output_samplerate = output_samplerate
            self.output_n_channels = output_n_channels
            self.output_bitdepth = output_bitdepth
            self.output_format = output_format

        clean_tmp_folder()
        self.raw_audio = ""

    def check_up(self):
        """
        TODO DOCUMENTATION
        :return:
        """
        check_audio_file(self.audio_path)
        audio_name = path.basename(self.audio_path).split('.')[0]
        audio_conv_path = convert_audio(self.audio_path,
                                        path.join(get_tmp_folder(), audio_name),
                                        self.output_samplerate,
                                        self.output_n_channels,
                                        self.output_bitdepth,
                                        get_working_format())

        self.raw_audio = audio_conv_path

    def clean_audio(self):
        """
        TODO DOCUMENTATION
        :return:
        """
        apply_filters(self.raw_audio)
        normalize_audio(self.raw_audio)
        noise_removal(self.raw_audio)
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
        clean_tmp_folder()
        print("PROCESAR SALIDA")
        pass
