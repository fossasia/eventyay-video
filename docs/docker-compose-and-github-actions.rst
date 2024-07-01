
Documentation for Docker Compose and GitHub Actions Workflow
=============================================================

Docker Compose File
--------------------

Overview
--------
This Docker Compose file is configured to set up a multi-service application, including a Venueless service, Redis instances, and a PostgreSQL database. The `TAG`, `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWD` environment variables are dynamically set and used within the services.

`docker-compose.yml`

        version: '3.4'

        services:
          venueless:
            image: eventyay/eventyay-video:${TAG}-latest
            container_name: venueless
            ports:
              - "8375:80"
            environment:
              - DJANGO_SETTINGS_MODULE=venueless.settings
              - LC_ALL=C.UTF-8
              - IPYTHONDIR=/data/.ipython
              - VENUELESS_COMMIT_SHA=${COMMIT}
              - VENUELESS_DB_TYPE=postgresql
              - VENUELESS_DB_NAME=${POSTGRES_DB}
              - VENUELESS_DB_USER=${POSTGRES_USER}
              - VENUELESS_DB_PASS=${POSTGRES_PASSWD}
              - VENUELESS_DB_HOST=venueless-db
              - VENUELESS_REDIS_URLS=redis://venueless-redis:6379/0,redis://venueless-redis1:6379/0
              - VENUELESS_DATA_DIR=/data
              - VENUELESS_MEDIA_URL=http://localhost:8375/media/
              - VENUELESS_REDIS_USE_PUBSUB=true
            depends_on:
              - venueless-db
              - venueless-redis
              - venueless-redis1
            volumes:
              - /etc/venueless:/etc/venueless
              - /data:/data
            entrypoint: ["/usr/local/bin/venueless"]
            command: ["all"]
          venueless-webapp:
            image: eventyay/eventyay-video:${TAG}-latest
            container_name: venueless-webapp
            ports:
              - "8002:8880"
            environment:
              - NODE_OPTIONS=--openssl-legacy-provider
            entrypoint: [""]
            command: ["npm", "start", "--", "--host", "0.0.0.0"]
            working_dir: /venueless/webapp

          venueless-redis:
            image: redis:latest
            container_name: venueless-redis

          venueless-redis1:
            image: redis:latest
            container_name: venueless-redis1

          venueless-db:
            image: postgres:15
            container_name: venueless-db
            volumes:
              - postgres_data:/var/lib/postgresql/data/
            environment:
              - POSTGRES_INITDB_ARGS=--auth-host=md5
              - POSTGRES_HOST_AUTH_METHOD=md5
              - POSTGRES_DB=${POSTGRES_DB}
              - POSTGRES_USER=${POSTGRES_USER}
              - POSTGRES_PASSWORD=${POSTGRES_PASSWD}

        volumes:
          postgres_data:
          appdata:

Usage
--------
Ensure that the `TAG`, `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWD` environment variables are set before running the Docker Compose commands. These variables are typically set in the deployment script or CI/CD pipeline.

GitHub Actions Workflow
------------------------

Overview
--------
This GitHub Actions workflow is configured to build and push Docker images to Docker Hub and deploy them to a remote server. The workflow is triggered on commits to the `development` and `master` branches and can also be manually triggered.

Workflow File (`main.yml`)

            name: Main workflow
            on:
              push:
                branches:
                  - development
                  - master
              workflow_dispatch:

            jobs:
              push_to_registry:
                name: Push Docker image to Docker Hub
                runs-on: ubuntu-latest
                steps:
                  - name: Check out the repo
                    uses: actions/checkout@v2

                  - name: Set up Docker tag
                    id: vars
                    run: echo "TAG=${GITHUB_REF##*/}" >> $GITHUB_ENV

                  - name: Log in to Docker Hub
                    uses: docker/login-action@v2
                    with:
                      username: ${{ secrets.DOCKER_USERNAME }}
                      password: ${{ secrets.DOCKER_PASSWORD }}

                  - name: Build and push Docker image
                    uses: docker/build-push-action@v2
                    with:
                      context: .
                      file: ./Dockerfile
                      push: true
                      tags: eventyay/eventyay-video:${{ env.TAG }}-latest
                      
              deploy:
                name: Deploy to server
                runs-on: ubuntu-latest
                needs: push_to_registry
                steps:
                - name: Check out the repo
                  uses: actions/checkout@v2
                - name: Set up Docker tag
                  id: vars
                  run: echo "TAG=${GITHUB_REF##*/}" >> $GITHUB_ENV
                - name: Deploy
                  run: |
                    mkdir -p ~/.ssh
                    chmod 700 ~/.ssh
                    eval "$(ssh-agent -s)"
                    echo "${{ secrets.SSH_PRIVATE_KEY }}" | ssh-add -
                    ssh-keyscan -H ${{ secrets.SERVER_HOST }} >> ~/.ssh/known_hosts
                    scp docker-compose.yml "${{ secrets.SERVER_USER }}@${{ secrets.SERVER_HOST }}:/home/eventyay/eventyay-videos"
                    ssh ${{ secrets.SERVER_USER }}@${{ secrets.SERVER_HOST }} "cd /home/eventyay/eventyay-videos && sudo docker pull eventyay/eventyay-video:${{ env.TAG }}-latest && sudo docker-compose up -d"


**Steps Explanation**


1. **Push to Registry Job**:
   - **Check out the repo**: Checks out the code from the repository.
   - **Set up Docker tag**: Sets the `TAG` environment variable based on the branch name.
   - **Log in to Docker Hub**: Logs in to Docker Hub using the provided secrets.
   - **Build and push Docker image**: Builds and pushes the Docker image using the `TAG`.

2. **Deploy Job**:
   - **Check out the repo**: Checks out the code from the repository.
   - **Set up Docker tag**: Sets the `TAG` environment variable based on the branch name.
   - **Setup SSH**: Sets up SSH for secure connection to the remote server.
   - **Copy docker-compose file**: Copies the `docker-compose.yml` file to the remote server.
   - **Deploy**: Connects to the remote server, sets the environment variables, pulls the Docker images, and runs `docker-compose` to start the services.

**Secrets Management**

Ensure the following secrets are set in your GitHub repository settings:
* `DOCKER_USERNAME`
* `DOCKER_PASSWORD`
* `SSH_PRIVATE_KEY`
* `SERVER_HOST`
* `SERVER_USER`

Usage
--------
1. **Trigger the Workflow**: The workflow triggers automatically on pushes to the `development` and `master` branches or can be manually triggered.
2. **Monitor the Workflow**: Monitor the workflow execution in GitHub Actions to ensure the Docker images are built, pushed, and deployed correctly.

Testing
--------
1. **Local Testing for docker-compose.yml**:
   - To test the Docker Compose file locally, set the required environment variables (`TAG`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWD`) and run the `docker-compose up` command.
   - Ensure that the services are up and running correctly and that the environment variables are correctly set.
2. **GitHub Actions Workflow Testing**:
   - Ensure the following secrets are set in your GitHub repository settings:
     * `DOCKER_USERNAME`
     * `DOCKER_PASSWORD`
     * `SSH_PRIVATE_KEY`
     * `SERVER_HOST`
     * `SERVER_USER`
    - Update the tags in the Docker Compose file and GitHub Actions workflow as needed.
    - Make changes to the codebase, commit the changes to the `development` or `master` branch or any other branch that triggers the workflow (please make sure that branch is added to the workflow trigger), and observe the workflow execution in GitHub Actions.
