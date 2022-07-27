FROM python:3.10

RUN mkdir FeedbackU



RUN python -m venv /opt/venv
ENV VIRTUAL_ENV /opt/venv
ENV PATH $VIRTUAL_ENV/bin:$PATH


WORKDIR ./FeedbackU

COPY . .

RUN pip install -r requirements.txt

