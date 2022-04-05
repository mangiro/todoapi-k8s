# ***TODO API with Kubernetes***
#### *Just a study of how to deploy a Kubernetes cluster locally.*
#
### **First of all**:
- To run the tests:
  - requirements:
    - Python ^3.8
    - [Poetry](https://python-poetry.org/docs/#installation)
```
poetry shell
poetry install
pytest
```
#
## **How to deploy it? (locally)**
- ### Requirements:
  - Docker
  - [minikube](https://minikube.sigs.k8s.io/docs/start/)
  - [kubectl](https://kubernetes.io/docs/tasks/tools/)
- ### Steps:
  1. Clone this repo and navigate to the root project folder `todoapi-k8s`.
  2. Start the cluster by running:
      ```
      minikube start
      ```
  3. To point your shell to minikube’s docker-daemon, run:
      ```
      eval $(minikube -p minikube docker-env)
      ```
      That way we can use our local docker images, without having to pull them from the docker hub:

  4. Now build the image in the Dockerfile:
      ```
      docker build . -t test-k8s/todoapp
      ```
  5. Apply a configuration to a resource by file name for pods generation:
      ```
      kubectl apply -f deployment.yml
      ```
  6. Finally run the following commands to list your application's pods and services:
      ```
      kubectl get pods
      kubectl get svc
      ```
      The following command will display the URL where your application is running, copy it and access it in your browser at the `/docs` endpoint:
      ```
      minikube service list
      ```
      Now you can interact with the API!

*NOTE: We are using only one replica of the application because SQLite is being used*

To view the logs, run the following command passing the name of your pod:
```
kubectl logs <name-of-the-pod-here>
```
