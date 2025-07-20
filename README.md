# 20250706-mongo-dump-cloud-run

## cmd

```sh
./venv/bin/python backup.py -M "$MONGO_URL" -B 20250706-for-mongo-dump -A mongo_gaq -C ./api-project-424250507607-af6dfaae7a25.json; ./venv/bin/python backup.py -M "$PYASSISTANTBOT_MONGO_URL" -B 20250706-for-mongo-dump -A mongo_s8 -C ./api-project-424250507607-af6dfaae7a25.json;
```
