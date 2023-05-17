# k8s-freepbx

## Storage
This PoC uses Vultr block storage.

1. Create secret to connect to Vultr API, by changing your Personal Access Token within the yaml and then run:
```
kubectl create -f storage/vultr_csi/secret.yaml
```

2. Install CSI driver in order to create a new StorageClass
```
kubectl apply -f storage/vultr_csi/install_csi-v0.9.0.yaml
```

3. Check if StorageClass has been created successfully
```
kubectl get storageclass
```

## Database deployment
Freepbx requires MySql/MariaDb

1. Create ConfigMap
```
kubectl apply -f mysql/configmap.yaml
```

2. Create services
```
kubectl apply -f mysql/services.yaml
```

3. Create secret:
```
kubectl create secret generic mysql-password --from-literal=password=YOURPASSWORD
```

4. Deploy
```
kubectl apply -f mysql/statefulset.yaml
```
The statefulset will claim a 10GB volume.

## Freebpx deployment
1. Create PersistenVolumeClaim
```
kubectl create -f freepbx/pvc.yml
```