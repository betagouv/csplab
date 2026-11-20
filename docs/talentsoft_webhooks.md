# Talentsoft Webhooks

Webhooks can be used to subscribe to certain events. When one of those events is triggered, Talentsoft will send a HTTP `POST` payload to the webhook's configured URL. Webhooks can be used to be notified about vacancies status changes, application progression, or candidate hiring.

By default, the mechanism to call peers to inform them of any change **is triggered every 15 minutes** but can be modified by the client.

## Documentation

- [API](https://developers.cegid.com/api-details#api=cegid-talentsoft-recruiting-customer&product=cegid-talentsoft#webhooks) (see "Webhooks" endpoints)
- [Webhooks](https://developers.cegid.com/docreference/BusinessUnits/Recruiting-developer-portal/webhooks/_index.html)

## Creating and deleting webhooks

Use the interactive script:

```sh
mise run ingestion:talentsoft:webhooks
```

It asks for:

1. the action: create or delete webhooks;
2. the Talentsoft instance, among the `back` credentials of `TALENTSOFT_CREDENTIALS` (loaded from Scaleway, see `env.d/ingestion-example`), or other credentials typed by hand (the client secret is not echoed);
3. to create: the callback URL (prod, demo or another URL) and the events, `vacancy_new vacancy_update vacancy_deleted vacancy_status` by default;
4. to delete: the `hookId`s to delete, separated by spaces, commas or new lines.

Nothing is sent to Talentsoft before a final confirmation.

The script then prints a summary to copy into Vaultwarden: date, instance, client ID, callback URL and the `hookId` of each event. Keep it: these `hookId`s are needed to delete webhooks later. If a creation fails, the script stops, the webhooks already created stay active, and their `hookId`s are still printed in the summary. After a deletion, update the Vaultwarden entry from the summary of deleted `hookId`s.

The script calls these endpoints, with a token from `POST {base_url}api/token` (`client_credentials` grant, `Customer` scope):

- `POST {base_url}api/system/v1/webhooks` with `{"event", "callbackUrl", "pingUrl"}`, which returns `data.hookId`;
- `DELETE {base_url}api/system/v1/webhooks/{hookId}`.
