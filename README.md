# 20250706-mongo-dump-cloud-run

## cmd

```sh
./venv/bin/python backup.py -M "$MONGO_URL" -B 20250706-for-mongo-dump -A mongo_gaq -C ./api-project-424250507607-af6dfaae7a25.json; ./venv/bin/python backup.py -M "$PYASSISTANTBOT_MONGO_URL" -B 20250706-for-mongo-dump -A mongo_s8 -C ./api-project-424250507607-af6dfaae7a25.json;
```

## deploy of Cloud Function

```sh
gcloud functions deploy mongo-backup \
  --gen2 \
  --runtime=python311 \
  --region=us-east1 \
  --source=. \
  --entry-point=entrypoint \
  --trigger-topic=mongo-dump-cloud-run \
  --set-secrets="MONGO_URL=mongo-url-gaq:latest,PYASSISTANTBOT_MONGO_URL=mongo-url-s8:latest" \
  --timeout=300
```

