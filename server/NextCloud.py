import docker
from docker.errors import ImageNotFound, APIError, NotFound
import time
# Create a Docker client
client = docker.from_env()  # Uses environment variables or default socket

def startNextCloud():
    try:
        try:
            client.images.get('nextcloud:latest')
        except ImageNotFound as e:
            print("Pulling NextCloud image")
            client.images.pull('nextcloud:latest')
        
        try:
            existing_container = client.containers.get('my_web_server')
            print("Container already exists...")
            return "Exists" # Exit the function after restarting
        except NotFound:
            pass  # If the container doesn't exist, proceed to create it

        # Start a container from an image
        container = client.containers.run(
            image='nextcloud:latest',  # Image name
            detach=True,           # Run in background
            ports={'80/tcp': 8080},
            name='my_web_server',    # Name your container
        )
        print(f"Container {container.id} started")

    except APIError as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

        
def stopContainer():
    container = client.containers.get('my_web_server')
    # Stop the container (graceful shutdown)
    container.stop()
    print(f"Container {container.id} stopped")

    # Remove the container
    container.remove()
    print(f"Container {container.id} removed")

def restartContainer():
    container = client.containers.get('my_web_server')
    container.restart()