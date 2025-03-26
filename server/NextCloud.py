import docker
import webbrowser
from docker.errors import ImageNotFound, APIError
# Create a Docker client
client = docker.from_env()  # Uses environment variables or default socket

def openContainer(container_name):
    container = client.containers.get(container_name)
    port = container.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']
    webbrowser.open(f'http://localhost:{port}')

def startNextCloud():
    try:
        client = docker.from_env()  # Uses environment variables or default socket

        try:
            client.images.get('nextcloud:latest')
        except ImageNotFound as e:
            print("Pulling NextCloud image")
            client.images.pull('nextcloud:latest')

        # Start a container from an image
        container = client.containers.run(
            image='nextcloud:latest',  # Image name
            detach=True,           # Run in background
            ports={'80/tcp': 8080},
            name='my_web_server'    # Name your container
        )
        print(f"Container {container.id} started")

    except APIError as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def stopContainer():
    # Get a specific container by name
    container = client.containers.get('my_web_server')

    # Stop the container (graceful shutdown)
    container.stop()
    print(f"Container {container.id} stopped")

    # Remove the container
    container.remove()
    print(f"Container {container.id} removed")

startNextCloud()

openContainer('my_web_server')