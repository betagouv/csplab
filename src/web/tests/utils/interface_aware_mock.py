import inspect
from typing import Union, get_origin

OPTIONAL_UNION_LENGTH = 2


def create_interface_aware_mock(interface_class):
    class InterfaceAwareMock:
        def __init__(self):
            self._storage = {}
            self._interface_methods = self._analyze_interface(interface_class)

        def _analyze_interface(self, interface_class):
            methods = {}
            for method_name in dir(interface_class):
                if method_name.startswith("_"):
                    continue
                try:
                    method = getattr(interface_class, method_name)
                    if callable(method):
                        sig = inspect.signature(method)
                        return_annotation = sig.return_annotation
                        is_async = inspect.iscoroutinefunction(method)
                        methods[method_name] = {
                            "return_type": return_annotation,
                            "is_async": is_async,
                        }
                except Exception:  # noqa
                    pass
            return methods

        def __getattr__(self, method_name):
            if method_name in self._interface_methods:
                method_info = self._interface_methods[method_name]
                return_type = method_info["return_type"]
                is_async = method_info["is_async"]
                return self._create_method_from_return_type(return_type, is_async)

            # Handle common test utility methods not in interface
            if method_name == "count":
                return lambda: len(self._storage)

            return lambda *args, **kwargs: None

        def _create_method_from_return_type(self, return_type, is_async):
            if is_async:

                async def async_auto_generated_method(*args, **kwargs):
                    result = self._get_return_value(return_type, args, **kwargs)
                    return result

                return async_auto_generated_method
            else:

                def sync_auto_generated_method(*args, **kwargs):
                    result = self._get_return_value(return_type, args, **kwargs)
                    return result

                return sync_auto_generated_method

        def _get_return_value(self, return_type, args, **kwargs):  # noqa
            if return_type is None or return_type is type(None):
                return self._handle_none_return_type(args)

            if return_type is int:
                return len(self._storage)

            origin = get_origin(return_type)
            if origin is tuple:
                return (list(self._storage.values()), False)
            if origin is list:
                filters = None
                if len(args) >= OPTIONAL_UNION_LENGTH and isinstance(args[1], dict):
                    filters = args[1]
                elif len(args) >= 1 and isinstance(args[0], dict):
                    filters = args[0]
                elif len(args) >= 1 and hasattr(args[0], "family_code"):
                    offer = args[0]
                    if offer.family_code is None:
                        return []
                    filters = {"offer_family_code": offer.family_code}

                if filters:
                    filtered_results = []
                    for entity in self._storage.values():
                        match = True
                        for key, value in filters.items():
                            if (
                                not hasattr(entity, key)
                                or getattr(entity, key) != value
                            ):
                                match = False
                                break
                        if match:
                            filtered_results.append(entity)
                    return filtered_results

                return list(self._storage.values())

            if origin is type(Union) or str(origin) == "typing.Union":
                args_types = getattr(return_type, "__args__", ())
                if (
                    len(args_types) == OPTIONAL_UNION_LENGTH
                    and type(None) in args_types
                ):
                    actual_type = next(t for t in args_types if t is not type(None))
                    return self._get_return_value(actual_type, args, **kwargs)

            return (
                self._handle_typed_dict_return(return_type, args)
                if self._is_typed_dict(return_type)
                else self._handle_entity_return(args)
                if return_type and hasattr(return_type, "__name__")
                else []
            )

        def _is_typed_dict(self, return_type):
            return (
                hasattr(return_type, "__annotations__")
                and hasattr(return_type, "__total__")
                and hasattr(return_type, "__required_keys__")
            )

        def _handle_none_return_type(self, args):
            if args and hasattr(args[0], "__iter__") and not isinstance(args[0], str):
                for entity in args[0]:
                    if hasattr(entity, "id"):
                        self._storage[entity.id] = entity
            elif args and hasattr(args[0], "id"):
                self._storage[args[0].id] = args[0]
                return args[0]
            else:
                self._storage.clear()
            return None

        def _handle_typed_dict_return(self, return_type, args):
            try:
                result_dict = {}
                entities_count = 0

                if (
                    args
                    and hasattr(args[0], "__iter__")
                    and not isinstance(args[0], str)
                ):
                    entities = args[0]
                    for entity in entities:
                        if hasattr(entity, "id"):
                            self._storage[entity.id] = entity
                    entities_count = len(entities)

                for i, (field_name, field_type) in enumerate(
                    return_type.__annotations__.items()
                ):
                    if field_type is int:
                        result_dict[field_name] = entities_count if i == 0 else 0
                    elif get_origin(field_type) is list:
                        result_dict[field_name] = []
                    else:
                        result_dict[field_name] = None
                return result_dict
            except Exception:
                return {}

        def _handle_entity_return(self, args):
            if args and hasattr(args[0], "id"):
                entity = args[0]
                self._storage[entity.id] = entity
                return entity
            elif args:
                entity_id = args[0]
                if entity_id in self._storage:
                    return self._storage[entity_id]
            return None

    return InterfaceAwareMock()
