import json
import os
import gc

import sox
from pydub import AudioSegment

from utils.IO import get_tmp_folder, get_tmp_splitted_folder


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


def noise_removal(origin_path, destination_path="", return_json=True):
    """
    TODO DOCUMENTATION
    :param return_json:
    :param origin_path:
    :param destination_path:
    :return:
    """
    gc.collect()
    if destination_path == "":
        destination_path = origin_path

    original_audio = AudioSegment.from_wav(origin_path)
    original_audio_splited = list(original_audio[::1])
    audio_chunks = []
    noise_chunks = []
    max_noise_duration = get_audio_config()['max_noise_duration']
    max_noise_level = get_audio_config()['max_noise_level']
    aux_noise = []
    for i, chunk in enumerate(original_audio_splited):
        data = (i, chunk)
        if chunk.dBFS > max_noise_level:
            if len(aux_noise) > max_noise_duration:
                noise_chunks += aux_noise
            else:
                audio_chunks += aux_noise
            aux_noise.clear()
            audio_chunks.append(data)
        else:  # SILENCE
            aux_noise.append(data)
        if len(noise_chunks) > 100000:
            break

    if len(aux_noise) > max_noise_duration:
        noise_chunks += aux_noise
    else:
        audio_chunks += aux_noise
    gc.collect()
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
    gc.collect()

    if destination_path == origin_path:
        destination_path_splited = os.path.splitext(destination_path)
        destination_path = destination_path_splited[0] + '_2' + destination_path_splited[1]
        noise_remove.build(origin_path, destination_path)
        os.remove(origin_path)
        os.rename(destination_path, origin_path)
    else:
        noise_remove.build(origin_path, destination_path)

    if return_json:
        from itertools import groupby, count
        audio_list = [(list(g)) for k, g in
                      groupby([*zip(*audio_chunks)][0], key=lambda i, j=count(): i - next(j))]
        return [(l[0], l[-1]) for l in audio_list]


def split_audio(origin_path, periods=[]) -> list:
    """
    TODO DOCUMENTATION
    :param origin_path:
    :param periods:
    :return:
    """
    gc.collect()
    original_audio = AudioSegment.from_wav(origin_path)
    original_audio_splited = list(original_audio[::1])
    del original_audio
    gc.collect()
    if len(periods) == 0:
        min_silence_duration = get_audio_config()['min_silence_duration']
        max_silence_level = get_audio_config()['max_silence_level']

        audio_chunks = []
        aux_silence = []
        # corte = int(len(original_audio_splited) / 50)
        for i, chunk in enumerate(original_audio_splited):
            # if i % corte == 0:
            #     print(i / corte, "%")
            if chunk.dBFS > max_silence_level:
                if len(aux_silence) < min_silence_duration:
                    audio_chunks += aux_silence
                aux_silence.clear()
                audio_chunks.append(i)

            else:  # SILENCE
                aux_silence.append(i)

        if len(aux_silence) < min_silence_duration:
            audio_chunks += aux_silence

        from itertools import groupby, count
        audio_list = [(list(g)) for k, g in
                      groupby(audio_chunks, key=lambda i, j=count(): i - next(j))]
        periods = [(l[0], l[-1]) for l in audio_list]

    audio_splited = [original_audio_splited[period[0]:period[1]] for period in periods]

    filenames = []
    info = []
    for i, segment in enumerate(audio_splited):
        audio_segment = sum(segment, AudioSegment.empty())
        filename = os.path.join(get_tmp_splitted_folder(), '{}.wav'.format(i))
        filenames.append(filename)
        info.append(periods[i])
        audio_segment.export(filename, format='wav')
    gc.collect()
    return filenames, info
