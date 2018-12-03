import sox
import json

def get_audio_config() -> dict:
    """
    TODO DOCUMENTATION
    :return:
    """
    audio_config_file = "src/configs/audio_config.json"
    audio_config = json.loads(open(audio_config_file).read())
    return audio_config


def get_working_format() -> str:
    working_format = get_audio_config()['working_format']
    return working_format


def convert_audio(origin_path, destination_path, samplerate, n_channels, bitdepth, output_format):
    """
    TODO DOCUMENTATION
    :param origin_path:
    :param destination_path:
    :param samplerate:
    :param n_channels:
    :param bitdepth:
    :param output_format:
    :return:
    """
    converter = sox.Transformer()
    converter.channels(n_channels)
    converter.convert(samplerate=samplerate, n_channels=n_channels, bitdepth=bitdepth)
    output_path = destination_path + '.' + output_format
    converter.build(origin_path, output_path)
    return output_path


if __name__ == '__main__':
    convert_audio(
        '/Users/pablomaciasmunoz/Dev/WS_Personal/S2T_AudioProcess/resources/audio/original/cadenaser_hoyporhoy_20180831_120000_122000_2.wav',
        '/Users/pablomaciasmunoz/Dev/WS_Personal/S2T_AudioProcess/resources/audio/out/cadenaser_hoyporhoy_20180831_120000_122000_2.wav',
        16000, 1, 16)
