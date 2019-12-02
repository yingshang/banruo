import json
import os
import warnings
from typing import List, Union, Tuple

import msgpack

from .utils import normalize_path


class ConfigNode(object):
    def __init__(self,
                 config_dict: dict,
                 path: List[str] = None,
                 strict_access: bool = True,
                 required_fields: List[Union[str, List[str]]] = None,
                 optional_fields: List[Union[str, List[str]]] = None):
        """
        Create a node in the Config Tree. This node will create its children if there are nested objects in the config.
        :param config_dict: Source dictionary containing the part of the config that will be in this node and its
                            children. Each dictionary value in this dictionary will become another ConfigNode that is
                            a child of this node.
        :param path: The access path to this node, i.e. the config keys that are used to access thos node.
        :param strict_access: If True, an error will be thrown if a non-existing field is accessed. If False,
                                    None will be returned instead.
        :param required_fields: A list of field names, for which an error will be thrown if they are accessed but don't
                                exist. These names either contain dots for the subfields or are already normalized
                                paths.
        :param optional_fields: A list of field names, for which None will be returned if they are accessed but don't
                                exist. These names either contain dots for the subfields or are already normalized
                                paths.
        """
        self.__path = path or []
        self.strict_access = strict_access

        self.required_fields, required_subfields = self.__parse_field_settings(required_fields or [])
        self.optional_fields, optional_subfields = self.__parse_field_settings(optional_fields or [])

        # parse the config dictionary and create children if necessary
        node_dict = {}
        for key, value in config_dict.items():
            if isinstance(value, dict):
                node_dict[key] = ConfigNode(value,
                                            path=self.__path + [key],
                                            strict_access=strict_access,
                                            required_fields=required_subfields,
                                            optional_fields=optional_subfields)
            else:
                node_dict[key] = value

        self.__node_dict = node_dict

    """
    Methods to access and modify the config contents.
    """
    def get(self, path: Union[str, List[str]]):
        """
        Retrieve a value in the config.
        If strict access is defined or the field is a required field, an AttributeError is thrown if the referenced
        field does not exist. Otherwise, i.e. non-strict access is defined or the field is an optional field, None is
        returned in the field does not exist.
        :raises AttributeError: Raised when a non-existing field is accessed when either strict access is defined or the
                                field is a required field.
        :param path: The key of the field. Can be either a string with '.' as delimiter of the nesting levels or a list
                     of keys with each element being one nesting level.
                     E.g., the string 'key1.key2' and list ['key1', 'key2'] reference the same config element.
        :return: The value of the referenced field.
        """
        path = normalize_path(path)
        key = path[0]
        try:
            value = self.__node_dict[key]
            if len(path) == 1:
                return value
            else:
                return value.get(path[1:])
        except KeyError as exception:
            if key in self.optional_fields or (not self.strict_access and key not in self.required_fields):
                return None
            else:
                raise AttributeError(f'No value exists for key "{self.__path_for_key(key)}"') from exception

    def add(self, path: Union[str, List[str]], value, overwrite: bool = True):
        """
        Add a new field to the config.
        :param path: The name of the field. Can be either a string with '.' as delimiter of the nesting levels or a list
                     of keys with each element being one nesting level.
                     E.g., the string 'key1.key2' and list ['key1', 'key2'] reference the same config element.
        :param value: The value that will be inserted. If this value is a dictionary it is transformed into
                      a ConfigNode.
        :param overwrite: If True, the value will be inserted if it already exists. Otherwise, a warning is printed.
        """
        path = normalize_path(path)
        key = path[0]
        if len(path) == 1:
            if isinstance(value, dict):
                self.__node_dict[key] = ConfigNode(value, path=self.__path + [key])
            else:
                if key in self.__node_dict and not overwrite:
                    warnings.warn(RuntimeWarning(f'Overwriting already existing key {self.__path_for_key(key)} '
                                                 f'(old value: "{self.__node_dict[key]}", new value: "{value}")'))
                self.__node_dict[key] = value
        else:
            if key not in self.__node_dict:
                self.__node_dict[key] = ConfigNode({}, path=self.__path + [key])
            self.get(key).add(path=path[1:], value=value, overwrite=overwrite)

    def update(self, path: Union[str, List[str]], value, upsert: bool = True) -> None:
        """
        Update field in the config.
        :param path: The name of the field. Can be either a string with '.' as delimiter of the nesting levels or a list
                     of keys with each element being one nesting level.
                     E.g., the string 'key1.key2' and list ['key1', 'key2'] reference the same config element.
        :param value: The value that should replace the old value. If this value is a dictionary it is transformed into
                      a ConfigNode.
        :param upsert: If True, the value will be inserted if it doesn't exist. Otherwise, an exception is raised.
        """
        path = normalize_path(path)
        key = path[0]
        if len(path) == 1:
            if key not in self.__node_dict and not upsert:
                raise RuntimeError(f"Updating not existing key {self.__path_for_key(key)}. To insert non existing keys"
                                   f"set upsert=True.")
            if isinstance(value, dict):
                self.__node_dict[key] = ConfigNode(value, path=self.__path + [key])
            else:
                self.__node_dict[key] = value
        else:
            if key not in self.__node_dict and upsert:
                self.__node_dict[key] = ConfigNode({}, path=self.__path + [key])
            elif key not in self.__node_dict:
                raise RuntimeError(f"Updating not existing key {self.__path_for_key(key)}. To insert non existing keys"
                                   f"set upsert=True.")
            self.get(key).update(path=path[1:], value=value, upsert=upsert)

    def merge_with_env_variables(self, prefix: Union[str, List[str]]):
        """
        Take all environment variables that start with the specified prefix or one of the specific prefixes and merge
        them into the config. These values overwrite existing ones.
        The environment variable names will be split on underscores (_) and changed to lowercase to determine the
        different keys (e.g., "FOO_BAR_TEST_ME" will result in the keys ["bar", "test", "me"] (with the prefix "FOO").
        :param prefix: Either a single or a list of prefixes of the environment variables (e.g., "FOO_").
        """
        prefixes = [prefix] if isinstance(prefix, str) else prefix
        for key in os.environ:
            for prefix in prefixes:
                if key.startswith(f"{prefix}_"):
                    value = os.environ[key]
                    cleaned_key = key[len(prefix) + 1:]
                    cleaned_key = cleaned_key.lower().split("_")
                    self.update(path=cleaned_key, value=value, upsert=True)

    """
    Iteration functions
    """
    def keys(self):
        for key, value in self.__node_dict.items():
            if isinstance(value, ConfigNode):
                yield from value.keys()
            else:
                yield self.__path_for_key(key)

    def values(self):
        for key, value in self.__node_dict.items():
            if isinstance(value, ConfigNode):
                yield from value.values()
            else:
                yield value

    def items(self):
        for key, value in self.__node_dict.items():
            if isinstance(value, ConfigNode):
                yield from value.items()
            else:
                yield self.__path_for_key(key), value

    """
    Serialization functions
    """
    def to_dict(self) -> dict:
        config_dict = {}
        for key, value in self.__node_dict.items():
            if isinstance(value, ConfigNode):
                config_dict[key] = value.to_dict()
            else:
                config_dict[key] = value
        return config_dict

    def to_json(self) -> str:
        """
        Serialize the config to a json dictionary/object. The default serialization method for non-JSON serializable
        types is just using their string representation (e.g., datetime.timedelta).
        :return: The JSON object of the config as string.
        """
        return json.dumps(self.to_dict(), default=str)

    def to_msgpack(self) -> bytes:
        """
        Serialize the config as a dictionary via msgpack. To handle unserializable data types, the config is first
        parsed to json (which converts every unparsable type to strings), parsed back and then serialized with msgpack.
        :return: The binary msgpack representation of the config.
        """
        return msgpack.dumps(json.loads(self.to_json()))

    @classmethod
    def from_msgpack(cls, data: bytes) -> 'ConfigNode':
        return cls(msgpack.loads(data, raw=False))

    """
    Built-in python functions
    """
    def __iter__(self):
        yield from self.keys()

    def __getattr__(self, item: str):
        """
        Enables access of config elements via dots (i.e. config.field1 instead of config["field1"]). This method wraps
        the get method.
        If strict access is defined or the field is a required field, an AttributeError is thrown if the referenced
        field does not exist. Otherwise, i.e. non-strict access is defined or the field is an optional field, None is
        returned in the field does not exist.
        :raises AttributeError: Raised when a non-existing field is accessed when either strict access is defined or the
                                field is a required field.
        :param item: the field that is accessed.
        :return: The value of the referenced field.
        """
        return self.get(item)

    def __contains__(self, item: Union[str, List[str]]) -> bool:
        """
        Test if a field exists in the config and is not None (result in the case of a non-existing optional field).
        If the field does not exist, an AttributeError is thrown, and therefore False is returned.
        :param item: The field whose existence is tested. Can be either a string with '.' as delimiter of the nesting
                     levels or a list of keys with each element being one nesting level.
                     E.g., the string 'key1.key2' and list ['key1', 'key2'] reference the same config element.
        :return: True if the field exists in the Config and False otherwise.
        """
        try:
            result = self.get(item)
            return result is not None
        except AttributeError:
            return False

    def __str__(self):
        return f"ConfigNode(path={self.__path}, values={self.__node_dict}, strict_access={self.strict_access}, " \
               f"required_fields={self.required_fields}, optional_fields={self.optional_fields})"

    __repr__ = __str__

    def __eq__(self, other):
        if isinstance(other, ConfigNode):
            return self.to_dict() == other.to_dict()
        else:
            return False

    def __getstate__(self):
        """
        This method is needed to enable pickling since this class overwrites __getattr__.
        """
        return vars(self)

    def __setstate__(self, state):
        """
        This method is needed to enable pickling since this class overwrites __getattr__.
        """
        vars(self).update(state)

    """
    Private functions used in this class (e.g., for utility).
    """
    @property
    def __path_str(self):
        return ".".join(self.__path)

    def __path_for_key(self, key: str):
        print_path = self.__path_str + "." * bool(self.__path)
        return print_path + key

    def __parse_field_settings(self, field_names: List[Union[str, List[str]]]) -> Tuple[List[str], List[List[str]]]:
        """
        Parses settings (required or optional) for fields and subfields of this node.
        :param field_names: A list of either field names containing dots or already normalized paths.
        :return: A tuple of first a list of the field names that are in this node and secondly a list of normalized
                 paths of subfields (i.e., fields in children of this node).
        """
        settings = []
        subfield_settings = []
        normalized_fields = [normalize_path(field) for field in field_names]
        for path in normalized_fields:
            if len(path) == 1:
                settings.append(path[0])
            else:
                subfield_settings.append(path[1:])
        return settings, subfield_settings


class Config(ConfigNode):
    def __init__(self,
                 config_dict: dict,
                 strict_access: bool = True,
                 required_fields: List[Union[str, List[str]]] = None,
                 optional_fields: List[Union[str, List[str]]] = None):
        super(Config, self).__init__(config_dict=config_dict,
                                     path=[],
                                     strict_access=strict_access,
                                     required_fields=required_fields,
                                     optional_fields=optional_fields)
