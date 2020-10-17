ARG PYTHON_VERSION
ARG WORKDIR
FROM python:$PYTHON_VERSION
WORKDIR /$WORKDIR
COPY binary_download.sh .
RUN sh binary_download.sh
COPY ToxicBot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ToxicBot/ .
CMD python app.py