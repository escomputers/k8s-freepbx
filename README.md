# k8s-freepbx
Run <a href="https://www.freepbx.org" target="_blank">FreePBX</a> (<a href="https://www.asterisk.org" target="_blank">Asterisk</a>) on <a href="https://kubernetes.io" target="_blank">Kubernetes.</a>

Just pure open source power.

## Storage
This PoC uses <a href="https://www.vultr.com/?ref=9460695" target="_blank">Vultr block storage.</a>

1. Create secret to connect to Vultr API, by changing your Personal Access Token within the yaml and then run:
```
kubectl create -f storage/vultr_csi/secret.yaml
```

2. Install CSI driver in order to create a new default StorageClass for dynamic volumes provisioning
```
kubectl apply -f storage/vultr_csi/install_csi-v0.9.0.yaml
```

3. Check if StorageClass has been created successfully
```
kubectl get storageclass
```

## Database deployment
Freepbx requires MySql/MariaDb

A statefulset of 3 replicas with one pod for WRITE operations and the others for READ ops.
1. Create ConfigMap
```
kubectl apply -f mysql/configmap.yaml
```

2. Create services
```
kubectl apply -f mysql/services.yaml
```

3. Deploy
```
kubectl apply -f mysql/statefulset.yaml
```

4. Test connection with READ operation
```
kubectl run mysql-client --image=mysql:5.7 -i -t --rm --restart=Never -- mysql -h mysql-read -e "SHOW DATABASES;"
```

or
```
kubectl run mysql-client-loop --image=mysql:5.7 -i -t --rm --restart=Never --\
  bash -ic "while sleep 1; do mysql -h mysql-read -e 'SELECT @@server_id,NOW()'; done"
```


## Freebpx deployment
<h5>TODO</h5>
1. Create PersistenVolumeClaim
```
kubectl create -f freepbx/pvc.yml
```

## Exposing services
1. Deploy <a href="https://github.com/kubernetes/ingress-nginx" target="_blank">nginx-controller</a> (read cloud provider docs to check features, in most cases a public IP address will be automatically allocated to it)
```
kubectl apply -f ingress/nginx-ingress-controller.yaml
```

2. Deploy cert-manager for TLS certificates
```
# TODO
```


### KUARD test
1. Deploy and expose <a href="https://github.com/kubernetes-up-and-running/kuard" target="_blank">KUARD</a> to test nginx-controller (keep order)
```
kubectl apply -f kuard/service.yaml
kubectl apply -f kuard/deployment.yaml
kubectl apply -f kuard/ingress.yaml
```

2. Check if web server within the pod is running
```
# PLAIN HTTP
kubectl run curl-client --image=curlimages/curl:8.1.0 -i -t --rm --restart=Never -- http://<PODIP>:8080
```

3. Check from outside
Open http://<YOURINGRESSFQDN>
