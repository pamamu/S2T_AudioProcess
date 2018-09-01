from os import path

import sox

from utils.IO import check_file, check_folder


class Audio:
    def __init__(self,
                 origin_path,
                 destination_path,
                 samplerate=16000,
                 n_channels=1,
                 bitdepth=16,
                 output_filename='full',
                 output_extension='wav'):
        self.origin_path = origin_path
        self.destination_path = destination_path
        self.filename, self.file_extension = check_file(self.origin_path)
        check_folder(self.destination_path, True)
        self.fullaudio_path = path.join(destination_path, output_filename + '.' + output_extension)
        self.convert(samplerate, n_channels, bitdepth, self.fullaudio_path)

    def convert(self, _samplerate, _n_channels, _bitdepth, output_file):
        """
        TODO

        :param _samplerate:
        :param _n_channels:
        :param _bitdepth:
        :param output_file:
        :return:
        """
        converter = sox.Transformer()
        converter.channels(_n_channels)
        converter.convert(samplerate=_samplerate, n_channels=_n_channels, bitdepth=_bitdepth)
        converter.build(self.origin_path, output_file)

    def split_audio(self):
        pass


if __name__ == '__main__':
    Audio(origin_path= '/home/pablo/Dev/TFG/S2T_AudioProcess/resources/audio/cadenaser_hoyporhoy_20180831_120000_122000_2.wav',
          destination_path= '/home/pablo/Dev/TFG/S2T_AudioProcess/resources/audio/prueba')
