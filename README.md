# 20250706-mongo-dump-cloud-run

## cmd

```sh
./venv/bin/python backup.py -M "$MONGO_URL" -B 20250706-for-mongo-dump -A mongo_gaq -C ./api-project-424250507607-af6dfaae7a25.json; ./venv/bin/python backup.py -M "$PYASSISTANTBOT_MONGO_URL" -B 20250706-for-mongo-dump -A mongo_s8 -C ./api-project-424250507607-af6dfaae7a25.json;
```

## deploy of Cloud Function

```sh
gcloud builds submit --tag gcr.io/$GCLOUD_PROJECT_ID/mongo-backup . && sleep 30 && gcloud run deploy mongo-backup \
  --image gcr.io/$GCLOUD_PROJECT_ID/mongo-backup \
  --region=us-east1 \
  --set-secrets="MONGO_URL=mongo-url-gaq:latest,PYASSISTANTBOT_MONGO_URL=mongo-url-s8:latest" \
  --timeout=300
```

