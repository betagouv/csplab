from domain.value_objects.webhook_type import WebhookType

SOURCE_TO_WEBHOOK_TYPE = {
    "talentsoft": WebhookType.OFFER,
}

WEBHOOK_TYPE_TO_SOURCE = {
    WebhookType.OFFER: "talentsoft",
}
