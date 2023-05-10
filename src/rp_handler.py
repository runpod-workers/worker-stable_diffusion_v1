''' infer.py for runpod worker '''

import os
import predict
import argparse

import runpod
from runpod.serverless.utils.rp_validator import validate
from runpod.serverless.utils.rp_upload import upload_file_to_bucket
from runpod.serverless.utils import rp_download, rp_cleanup

from rp_schema import INPUT_SCHEMA


# Grab args
parser = argparse.ArgumentParser()
parser.add_argument('--model_tag', type=str, default="runwayml/stable-diffusion-v1-5")
args = parser.parse_args()

MODEL = predict.Predictor(model_tag=args.model_tag)
MODEL.setup()


def run(job):
    '''
    Run inference on the model.
    Returns output path, width the seed used to generate the image.
    '''
    job_input = job['input']

    # Input validation
    validated_input = validate(job_input, INPUT_SCHEMA)

    if 'errors' in validated_input:
        return {"error": validated_input['errors']}
    validated_input = validated_input['validated_input']

    # Download input objects
    job_input['init_image'], job_input['mask'] = rp_download.download_files_from_urls(
        job['id'],
        [job_input.get('init_image', None), job_input.get(
            'mask', None)]
    )  # pylint: disable=unbalanced-tuple-unpacking

    MODEL.NSFW = job_input.get('nsfw', True)

    if job_input['seed'] is None:
        job_input['seed'] = int.from_bytes(os.urandom(2), "big")

    img_paths = MODEL.predict(
        prompt=job_input["prompt"],
        negative_prompt=job_input.get("negative_prompt", None),
        width=job_input.get('width', 512),
        height=job_input.get('height', 512),
        init_image=job_input['init_image'],
        mask=job_input['mask'],
        prompt_strength=job_input['prompt_strength'],
        num_outputs=job_input.get('num_outputs', 1),
        num_inference_steps=job_input.get('num_inference_steps', 50),
        guidance_scale=job_input['guidance_scale'],
        scheduler=job_input.get('scheduler', "K-LMS"),
        lora=job_input.get("lora", None),
        lora_scale=job_input.get("lora_scale", 1),
        seed=job_input['seed']
    )

    job_output = []
    for index, img_path in enumerate(img_paths):
        image_url = upload_file_to_bucket(job['id'], img_path, index)

        job_output.append({
            "image": image_url,
            "seed": job_input['seed'] + index
        })

    # Remove downloaded input objects
    rp_cleanup.clean(['input_objects'])

    return job_output


runpod.serverless.start({"handler": run})
