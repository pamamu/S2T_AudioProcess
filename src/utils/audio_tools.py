import sox
import os
import json
from pydub import AudioSegment, silence
from utils.IO import get_tmp_folder
from pydub.playback import play


def get_audio_config() -> dict:
    """
    TODO DOCUMENTATION
    :return:
    """
    audio_config_file = "src/configs/audio_config.json"
    audio_config = json.loads(open(audio_config_file).read())
    return audio_config


def get_working_format() -> str:
    """
    TODO DOCUMENTATION
    :return:
    """
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


def apply_filters(origin_path, destination_path=""):
    """
    TODO DOCUMENTATION
    :param origin_path:
    :param destination_path:
    :return:
    """
    if destination_path == "":
        destination_path = origin_path
    noise_removal = sox.Transformer()
    noise_removal.lowpass(3000)
    noise_removal.highpass(200)
    if destination_path == origin_path:
        destination_path_splited = os.path.splitext(destination_path)
        destination_path = destination_path_splited[0] + '_2' + destination_path_splited[1]
        noise_removal.build(origin_path, destination_path)
        os.remove(origin_path)
        os.rename(destination_path, origin_path)
    else:
        noise_removal.build(origin_path, destination_path)


def vad(origin_path, destination_path=""):
    """
    TODO DOCUMENTATION
    :param origin_path:
    :param destination_path:
    :return:
    """
    if destination_path == "":
        destination_path = origin_path
    vad = sox.Transformer()
    vad.vad(1, True)
    if destination_path == origin_path:
        destination_path_splited = os.path.splitext(destination_path)
        destination_path = destination_path_splited[0] + '_2' + destination_path_splited[1]
        vad.build(origin_path, destination_path)
        os.remove(origin_path)
        os.rename(destination_path, origin_path)
    else:
        vad.build(origin_path, destination_path)


def normalize_audio(origin_path, destination_path=""):
    """
    TODO DOCUMENTATION
    :param origin_path:
    :param destination_path:
    :return:
    """
    if destination_path == "":
        destination_path = origin_path
    normalize = sox.Transformer()
    normalize.norm()
    if destination_path == origin_path:
        destination_path_splited = os.path.splitext(destination_path)
        destination_path = destination_path_splited[0] + '_2' + destination_path_splited[1]
        normalize.build(origin_path, destination_path)
        os.remove(origin_path)
        os.rename(destination_path, origin_path)
    else:
        normalize.build(origin_path, destination_path)


def noise_removal(origin_path, destination_path=""):
    """
    TODO DOCUMENTATION
    :param origin_path:
    :param destination_path:
    :return:
    """
    if destination_path == "":
        destination_path = origin_path

    original_audio = AudioSegment.from_wav(origin_path)
    original_audio_splited = list(original_audio[::1])
    audio_chunks = []
    noise_chunks = []
    max_noise_duration = get_audio_config()['max_noise_duration']
    aux_noise = []

    for i, chunk in enumerate(original_audio_splited):
        data = (i, chunk)
        if chunk.dBFS > -25:
            if len(aux_noise) > max_noise_duration:
                noise_chunks += aux_noise
            else:
                audio_chunks += aux_noise
            aux_noise.clear()
            audio_chunks.append(data)

        else:  # SILENCE
            aux_noise.append(data)

    if len(aux_noise) > max_noise_duration:
        noise_chunks += aux_noise
    else:
        audio_chunks += aux_noise

    # try:
    #     raw_audio = sum([*zip(*audio_chunks)][1], AudioSegment.empty())
    # except IndexError:
    #     raw_audio = AudioSegment.empty()
    # raw_audio_path = os.path.join(get_tmp_folder(), 'raw_audio.wav')
    # raw_audio.export(raw_audio_path, format='wav')

    try:
        raw_noise = sum([*zip(*noise_chunks)][1], AudioSegment.empty())
    except IndexError:
        raw_noise = AudioSegment.empty()
    raw_noise_path = os.path.join(get_tmp_folder(), 'raw_noise.wav')
    raw_noise.export(raw_noise_path, format='wav')

    noise_reduction = sox.Transformer()
    noise_prof_path = os.path.join(get_tmp_folder(), 'noise.prof')
    noise_reduction.noiseprof(raw_noise_path, noise_prof_path)

    noise_remove = sox.Transformer()
    noise_tolerance = get_audio_config()['noise_tolerance']
    noise_remove.noisered(noise_prof_path, noise_tolerance)

    if destination_path == origin_path:
        destination_path_splited = os.path.splitext(destination_path)
        destination_path = destination_path_splited[0] + '_2' + destination_path_splited[1]
        noise_remove.build(origin_path, destination_path)
        os.remove(origin_path)
        os.rename(destination_path, origin_path)
    else:
        noise_remove.build(origin_path, destination_path)
