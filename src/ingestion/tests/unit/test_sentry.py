from api._sentry import scrub_dict, strip_sentry_sensitive_data


class TestScrubDict:
    def test_filters_sensitive_keys(self):
        data = {"password": "secret", "token": "abc", "name": "Alice"}
        result = scrub_dict(data)
        assert result["password"] == "[Filtered]"
        assert result["token"] == "[Filtered]"
        assert result["name"] == "Alice"

    def test_filtering_is_case_insensitive(self):
        data = {"Authorization": "Bearer token", "Content-Type": "application/json"}
        result = scrub_dict(data)
        assert result["Authorization"] == "[Filtered]"
        assert result["Content-Type"] == "application/json"

    def test_empty_dict(self):
        assert scrub_dict({}) == {}

    def test_no_sensitive_keys(self):
        data = {"foo": "bar", "baz": 42}
        assert scrub_dict(data) == {"foo": "bar", "baz": 42}


class TestStripSentrySensitiveData:
    def test_scrubs_request_data(self):
        event = {"request": {"data": {"password": "secret", "username": "alice"}}}
        result = strip_sentry_sensitive_data(event, {})
        assert result["request"]["data"]["password"] == "[Filtered]"
        assert result["request"]["data"]["username"] == "[Filtered]"

    def test_scrubs_request_headers(self):
        event = {
            "request": {
                "headers": {
                    "Authorization": "Bearer token",
                    "Accept": "application/json",
                }
            }
        }
        result = strip_sentry_sensitive_data(event, {})
        assert result["request"]["headers"]["Authorization"] == "[Filtered]"
        assert result["request"]["headers"]["Accept"] == "application/json"

    def test_ignores_non_dict_request_data(self):
        event = {"request": {"data": "raw-body-string"}}
        result = strip_sentry_sensitive_data(event, {})
        assert result["request"]["data"] == "raw-body-string"

    def test_handles_event_without_request(self):
        event = {"level": "error"}
        result = strip_sentry_sensitive_data(event, {})
        assert result == {"level": "error"}
