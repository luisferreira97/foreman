import json
import logging
from pathlib import Path


def load_json(path: str) -> dict:
    """
    Load a JSON file and return it as a dictionary.
    
    Args:
        path (str): The path to the JSON file.
        
    Returns:
        dict: The JSON file as a dictionary.
    """
    
    doc = json.loads(Path(path).read_text())

    return doc


def save_json(data: dict, path: str) -> None:
    """
    Save a dictionary as a JSON file.
    
    Args:
        data (dict): The dictionary to save.
        path (str): The path to save the JSON file.
    """
    
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)


def filter_source_keys(doc: dict, keys_to_keep: list) -> dict:
    """
    Filter the documentation file to only include the given keys.

    Args:
        doc (dict): The documentation file as a dictionary.
        keys_to_keep (list): The keys to keep in the documentation file.
    Returns:
        dict: The filtered documentation file as a dictionary.
    """

    for source in doc:
        doc[source] = {key: value for key, value in doc[source].items() if key in keys_to_keep}

    return doc


def filter_column_keys(doc: dict, column_keys_to_keep: list) -> dict:
    """
    Filter the documentation file to only include the given keys.

    Args:
        doc (dict): The documentation file as a dictionary.
        keys_to_keep (list): The keys to keep in the documentation file.
    Returns:
        dict: The filtered documentation file as a dictionary.
    """

    for source in doc:
        for column in doc[source]["columns"]:
            doc[source]["columns"][column] = {key: value for key, value in doc[source]["columns"][column].items() if key in column_keys_to_keep}

    return doc


def filter_metadata_keys(doc: dict, metadata_keys_to_keep: list) -> dict:
    """
    Filter the documentation file to only include the given keys.

    Args:
        doc (dict): The documentation file as a dictionary.
        keys_to_keep (list): The keys to keep in the documentation file.
    Returns:
        dict: The filtered documentation file as a dictionary.
    """

    for source in doc:
        for column in doc[source]["metadata"]:
            doc[source]["metadata"] = {key: value for key, value in doc[source]["metadata"].items() if key in metadata_keys_to_keep}

    return doc


def change_table_name_format(doc: dict) -> dict:
    """
    Change the table name format to be more readable.
    Original format: <type>.<project>.<table>
    New format: <table>

    Args:
        doc (dict): The documentation file as a dictionary.
    Returns:
        dict: The documentation file with the table names in a more readable format.
    """

    sources = list(doc.keys())

    for source in sources:
        new_key_name = source.split(".")[-1]
        doc[new_key_name] = doc.copy()[source]
        del doc[source]

    return doc


def harmonize_data_types(doc: dict) -> dict:
    """
    Harmonize the data types in the documentation file.
    'varchar(x)' -> 'text'
    'decimal' -> 'float' # the type 'float' also exists
    'big int' or 'integer' -> 'int'

    Args:
        doc (dict): The documentation file as a dictionary.
    Returns:
        dict: The documentation file with the data types harmonized.
    """

    for source in doc:
        for column in doc[source]["columns"]:
            if "varchar" in doc[source]["columns"][column]["type"]:
                doc[source]["columns"][column]["type"] = "string"
            elif "decimal" in doc[source]["columns"][column]["type"]:
                doc[source]["columns"][column]["type"] = "float"
            elif doc[source]["columns"][column]["type"] in ["bigint", "integer"]:
                doc[source]["columns"][column]["type"] = "int"

    return doc


def process_manifest(manifest: dict) -> dict:
    """
    Process the manifest file and return the manifest as a dictionary.

    Args:
        manifest_path (str): The path to the manifest file.
    Returns:
        dict: The manifest as a dictionary.
    """

    logging.info("Starting manifest processing")

    manifest = manifest["nodes"]

    manifest = filter_source_keys(manifest, ["schema", "description", "columns"])
    logging.info("Successfully filtered source keys")

    manifest = filter_column_keys(manifest, ["description", "type"])
    logging.info("Successfully filtered column keys")

    manifest = change_table_name_format(manifest)
    logging.info("Successfully changed table name format")

    logging.info("Finishing manifest processing")

    return manifest


if __name__ == "__main__":
    manifest = load_json('../warehouse/target/manifest.json')
    manifest = process_manifest(manifest)
    save_json(manifest, 'docs.json')