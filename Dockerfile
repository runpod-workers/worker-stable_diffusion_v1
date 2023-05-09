FROM runpod/pytorch:3.10-2.0.0-117

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /

# Build args
ARG MODEL_URL
ENV MODEL_URL=${MODEL_URL}
ARG MODEL_NAME
ENV MODEL_NAME=${MODEL_NAME}

# Install Python dependencies (Worker Template)
COPY builder/requirements.txt /requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /requirements.txt && \
    rm /requirements.txt

# Fetch the model
COPY builder/model_fetcher.py /model_fetcher.py
RUN python /model_fetcher.py --model_url=${MODEL_URL}
RUN rm /model_fetcher.py

# Add src files (Worker Template)
ADD src .

CMD [ "python", "-u", "/rp_handler.py" ]
