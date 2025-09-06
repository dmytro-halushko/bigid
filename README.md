How to configure image repo:
Currently the workflow push the image into public dockerhub repo kinzeasy/bigid-dmyh. Credentials are stored in Github secrets.

DOCKERHUB_USERNAME - username
DOCKERHUB_TOKEN - access token

To configure other repo, you need to craete your own dockerhub access token and paste them into your Github account.

Kubernetes settings:

To create staging namespace:

kubectl create namespace staging

create secret in Kubernetes:

kubectl create secret generic bigid-dmyh-app-users --from-file=users.txt -n staging

