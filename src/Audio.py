"""
TODO DOCUMENTATION
"""

from os import path

from utils.IO import check_audio_file, get_tmp_folder, clean_tmp_folder, move_files, save_json
from utils.audio_tools import convert_audio, get_working_format, apply_filters, normalize_audio, noise_removal, \
    split_audio


class Audio:

    def __init__(self,
                 audio_path=None,
                 output_samplerate=None,
                 output_n_channels=None,
                 output_bitdepth=None,
                 output_format=None,
                 output_folder=None,
                 data=None):

        required_params = ['audio_path',
                           'output_samplerate',
                           'output_n_channels',
                           'output_bitdepth',
                           'output_format',
                           'output_folder']
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
            self.output_folder = output_folder

        clean_tmp_folder()
        self.raw_audio = ""
        self.audio_paths = []
        self.audio_name = ""
        self.info_audios = []

    def check_up(self):
        """
        TODO DOCUMENTATION
        :return:
        """
        check_audio_file(self.audio_path)
        self.audio_name = path.basename(self.audio_path).split('.')[0]
        audio_conv_path = convert_audio(self.audio_path,
                                        path.join(get_tmp_folder(), self.audio_name),
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
        print("\t\tFILTROS OK")
        normalize_audio(self.raw_audio)
        print("\t\tNORMALIZACION OK")
        noise_removal(self.raw_audio)
        print("\t\tREDUCCION DE RUIDO OK")

    def split_audio(self):
        """
        TODO DOCUMENTATION
        :return:
        """
        self.audio_paths, self.info_audios = split_audio(self.raw_audio)

    def process_output(self):
        """
        TODO DOCUMENTATION
        :return:
        """
        destination_paths = move_files(self.audio_paths, self.output_folder, self.audio_name)
        out = [{'path': audio_path,
                'start_time': info[0] / 1000,
                'end_time': info[1] / 1000
                } for audio_path, info in zip(destination_paths, self.info_audios)]
        destination_json = save_json(out, self.output_folder, self.audio_name)
        clean_tmp_folder()
        print("PROCESAR SALIDA")
        pass
