# Talentsoft Webhooks

Webhooks can be used to subscribe to certain events. When one of those events is triggered, Talentsoft will send a HTTP `POST` payload to the webhook's configured URL. Webhooks can be used to be notified about vacancies status changes, application progression, or candidate hiring.

By default, the mechanism to call peers to inform them of any change **is triggered every 15 minutes** but can be modified by the client.

## Documentation

- [API](https://developers.cegid.com/api-details#api=cegid-talentsoft-recruiting-customer&product=cegid-talentsoft#webhooks) (see "Webhooks" endpoints)
- [Webhooks](https://developers.cegid.com/docreference/BusinessUnits/Recruiting-developer-portal/webhooks/_index.html)

## Subscribing to events

The following script can be used to subscribe to `vacancy_*` events.

⚠️ Make a note of the various `hookId`! We need these IDs if we need to delete hooks.

```sh
set -e

cd src/ingestion

CALLBACK_URL="https://csplab-worker.osc-fr1.scalingo.io/webhooks/talentsoft"
EVENTS=(vacancy_new vacancy_update vacancy_deleted vacancy_status)

# Get an OAuth token
TOKEN=$(curl -s -d "client_id=${TALENTSOFT_BACK_CLIENT_ID}&client_secret=${TALENTSOFT_BACK_CLIENT_SECRET}&grant_type=client_credentials&scope=Customer" -X POST "${TALENTSOFT_BACK_BASE_URL}api/token" | jq -r '.access_token')

# Subscribe $CALLBACK_URL to these events
for event in "${EVENTS[@]}"; do
    echo "Registering $event…"
    RESPONSE=$(curl -s -w "\n%{http_code}" \
      -H "Authorization: Bearer ${TOKEN}" \
      -H "Content-Type: application/json" \
      -d "{\"event\": \"${event}\", \"callbackUrl\": \"${CALLBACK_URL}\", \"pingUrl\": \"${CALLBACK_URL}\"}" \
      -X POST "${TALENTSOFT_BACK_BASE_URL}api/system/v1/webhooks")
    HTTP_CODE=$(echo "$RESPONSE" | tail -1)
    BODY=$(echo "$RESPONSE" | sed '$d')
    HOOK_ID=$(echo "$BODY" | jq -r '.data.hookId')
    echo "HTTP $HTTP_CODE — hookId: $HOOK_ID"
    [[ "$HTTP_CODE" =~ ^2 ]] || { echo "Failed for $event, stopping."; exit 1; }
done
```

## Deleting a hook

The following script can be used to unregister a webhook by its `hookId`.

```sh
set -e

cd src/ingestion

HOOK_ID="<hookId>"

# Get an OAuth token
TOKEN=$(curl -s -d "client_id=${TALENTSOFT_BACK_CLIENT_ID}&client_secret=${TALENTSOFT_BACK_CLIENT_SECRET}&grant_type=client_credentials&scope=Customer" -X POST "${TALENTSOFT_BACK_BASE_URL}api/token" | jq -r '.access_token')

# Delete the webhook
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -X DELETE "${TALENTSOFT_BACK_BASE_URL}api/system/v1/webhooks/${HOOK_ID}")
echo "HTTP $HTTP_CODE"
[[ "$HTTP_CODE" =~ ^2 ]] || { echo "Failed to delete hookId ${HOOK_ID}."; exit 1; }
echo "Deleted hookId ${HOOK_ID}."
```
