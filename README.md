<div align="center">

<h1>Stable Diffusion v1.5 | Worker</h1>

[![Docker Image](https://github.com/runpod-workers/worker-stable_diffusion_v1/actions/workflows/CD-docker_release.yml/badge.svg)](https://github.com/runpod-workers/worker-stable_diffusion_v1/actions/workflows/CD-docker_release.yml)

</div>

## RunPod Endpoint

This repository contains the worker for the SDv1 AI Endpoints. The following docs can be referenced to make direct calls to the running endpoints on runpod.io

- [Stable Diffusion v1](https://docs.runpod.io/reference/stable-diffusion-v1)
- [Anything v3](https://docs.runpod.io/reference/anything-v3)
- [Anything v4](https://docs.runpod.io/reference/anything-v4)
- [OpenJourney](https://docs.runpod.io/reference/openjourney-sd-v15)

## Docker Image

The docker image requires two build arguments `MODEL_URL` and `Model_TAG` to build the image. The `MODEL_URL` is the url of the model repository and the `Model_TAG` is the tag of the model repository.

```bash
docker build --build-arg MODEL_URL=https://huggingface.co/runwayml/stable-diffusion-v1-5 --build-arg MODEL_TAG=main -t runwayml/stable-diffusion-v1-5 .
```

## Continuous Deployment

This worker follows a modified version of the [worker template](https://github.com/runpod-workers/worker-template) where the Docker build workflow contains additional SD models to be built and pushed.
