import docker
import os
import requests

client = docker.from_env()

def build_image(folder_path):
    print('Building image...')
    tag = os.path.basename(folder_path)
    
    try:
        client.images.build(
        path = folder_path,
        tag = tag,
        dockerfile = 'Dockerfile')

    except (docker.errors.BuildError, docker.errors.APIError, TypeError) as e:
        print(e)

    return tag

def run_container(image_tag, name, output_volume, entrypoint, timeout):
    print('Running container...')

    try:

        client.containers.run(image=image_tag, 
                              name=name,
                              entrypoint=entrypoint,
                              volumes=[f'{output_volume}:/output'],
                              auto_remove=True)
    
    except (docker.errors.ContainerError, docker.errors.ImageNotFound, docker.errors.APIError) as e:
        print(e)

    client.images.remove(image=image_tag, force=True)
