PUBLIC_PATH = "/api"


def preprocess_public_only(endpoints, **kwargs):
    selected_endpoints = []
    for path, path_regex, method, callback in endpoints:
        if path.startswith(PUBLIC_PATH):
            selected_endpoints.append((path, path_regex, method, callback))
    return selected_endpoints


def preprocess_internal_only(endpoints, **kwargs):
    selected_endpoints = []
    for path, path_regex, method, callback in endpoints:
        if not path.startswith(PUBLIC_PATH):
            selected_endpoints.append((path, path_regex, method, callback))
    return selected_endpoints
