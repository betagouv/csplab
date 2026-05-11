# Talentsoft Webhooks

Webhooks can be used to subscribe to certain events. When one of those events is triggered, Talentsoft will send a HTTP `POST` payload to the webhook's configured URL. Webhooks can be used to be notified about vacancies status changes, application progression, or candidate hiring.

By default, the mechanism to call peers to inform them of any change **is triggered every 15 minutes** but can be modified by the client.

## Documentation

- [API](https://developers.cegid.com/api-details#api=cegid-talentsoft-recruiting-customer&product=cegid-talentsoft#webhooks) (see "Webhooks" endpoints)
- [Webhooks](https://developers.cegid.com/docreference/BusinessUnits/Recruiting-developer-portal/webhooks/_index.html)

## Subscribing to events

The following script can be used to subscribe to `vacancy_*` events.

```sh
cd src/tycho

CALLBACK_URL="https://csplab-worker.osc-fr1.scalingo.io/webhooks/talentsoft"
EVENTS=(vacancy_new vacancy_update vacancy_deleted vacancy_status)

# Get an OAuth token
TOKEN=$(curl -s -d "client_id=${TYCHO_TALENTSOFT_BACK_CLIENT_ID}&client_secret=${TYCHO_TALENTSOFT_BACK_CLIENT_SECRET}&grant_type=client_credentials&scope=Customer" -X POST "${TYCHO_TALENTSOFT_BACK_BASE_URL}api/token" | jq -r '.access_token')

# Subscribe $CALLBACK_URL to these events
for event in "${EVENTS[@]}"; do
    echo "Registering $event…"
    curl -s -o /dev/null -w "%{http_code}" \
      -H "Authorization: Bearer ${TOKEN}" \
      -H "Content-Type: application/json" \
      -d "{\"event\": \"${event}\", \"callbackUrl\": \"${CALLBACK_URL}\", \"pingUrl\": \"${CALLBACK_URL}\"}" \
      -X POST "${TYCHO_TALENTSOFT_BACK_BASE_URL}api/system/v1/webhooks"
    echo ""
done
```
