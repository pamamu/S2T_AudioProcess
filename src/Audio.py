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
        # TODO Comprobar que existen los ficheros de configuracion
        # TODO Cargar ficheros de configuracion
        # TODO Comprobar informacion de ficheros de configuracion
        # TODO Comprobar Audio-Configuracion
        pass

    def clean_audio(self):
        pass

    def split_audio(self):
        pass

    def process_output(self):
        pass

# self.origin_path = origin_path
# self.destination_path = destination_path
# self.filename, self.file_extension = check_file(self.origin_path)
# check_folder(self.destination_path, True)
# self.fullaudio_path = path.join(destination_path, output_filename + '.' + output_extension)
# self.convert(samplerate, n_channels, bitdepth, self.fullaudio_path)

# def convert(self, _samplerate, _n_channels, _bitdepth, output_file):
#     """
#     TODO
#
#     :param _samplerate:
#     :param _n_channels:
#     :param _bitdepth:
#     :param output_file:
#     :return:
#     """
#     converter = sox.Transformer()
#     converter.channels(_n_channels)
#     converter.convert(samplerate=_samplerate, n_channels=_n_channels, bitdepth=_bitdepth)
#     converter.build(self.origin_path, output_file)
#
# def split_audio(self):
#     pass
