FROM pamamu/s2t_main-controller

ARG SHARED_FOLDER
ENV SHARED_FOLDER = $SHARED_FOLDER
ARG AUDIO_PROCESS_NAME
ENV AUDIO_PROCESS_NAME = $AUDIO_PROCESS_NAME

WORKDIR /srv/S2T/S2T_AudioProcess

ADD . .

RUN apk add --update sox ffmpeg
RUN pip install -r requirements.txt

CMD python src/app.py $AUDIO_PROCESS_NAME $SHARED_FOLDER

