"""
 information file routines
"""
# Standard library modules
import json
# import pprint
from pathlib import Path
# import os.path
import sys
import pkg_resources
import urllib.request

# Non-standard modules
import jsonschema
# import jsonref
import yaml

# Local modules
from .yamlref import load as yamlref_load, loads as yamlref_loads
from .info_dict import InfoDict

root_symbol = "#"
VALID_FORMATS = ["JSON", "YAML"]
VALID_TYPES = ["campaign", "experiment"]


def list_valid_types():
    """
    Returns a list of valid information file types
    """
    return VALID_TYPES


def get_information_file_type(filename):
    """
    Determines the type of a file from the filename

    Assumes that the filename is "*.{TYPE}.{SOMETHING}
    """

    the_type = Path(filename).name.split(".")[-2].lower()
    if the_type in VALID_TYPES:
        return the_type
    print(f"Unknown type: {the_type}")
    sys.exit(1)


def validate(filename, format=None, type=None, verbose=False,
             schema_file=None, quiet=False):
    """
    Validates a YAML or JSON file against schema
    type: "campaign" or "experiment"
    format: "JSON" or "YAML"

    if type and/or format are not provided, tries to figure them out from the
    filename, which should be "*{TYPE}.{FORMAT}
    """

    if quiet:
       verbose = False

    if not type and not schema_file:
        type = get_information_file_type(filename)

    assert type in VALID_TYPES, f'type "{type}" not in "{VALID_TYPES}"'

    if verbose:
        print(f"instance = {filename}")
    elif not quiet:
        print(f"instance = {Path(filename).name} ... ", end="")

    instance = _read_json_yaml_ref(filename, format=format)
    # instance = read_json_yaml(filename, format=format)

    if not schema_file:
        schema_file = pkg_resources.resource_filename(
            "campaigninfo",
            str(Path("data") / f"{type}.schema.json"))
    base_uri = "file://{}/".format(
        urllib.request.pathname2url(str(Path(schema_file).parent)))
    with open(schema_file, "r") as f:
        try:
            schema = yamlref_loads(f.read(), base_uri=base_uri,
                                   jsonschema=True)
        except json.decoder.JSONDecodeError as e:
            print("JSONDecodeError: Error loading JSON schema file: {}"
                  .format(schema_file))
            print(str(e))
            return False
        except Exception:
            print(f"Error loading JSON schema file: {schema_file}")
            print(sys.exc_info()[1])
            return False

    # Lazily report all errors in the instance
    # ASSUMES SCHEMA IS DRAFT-04 (I couldn't get it to work otherwise)
    try:
        if verbose:
            print(f"schema =   {Path(schema_file).name}")
            print("\tTesting schema ...", end="")

        # jsonschema.validate(instance, schema)
        v = jsonschema.Draft7Validator(schema)

        if verbose:
            print("OK")
            print("\tTesting instance ...", end="")
        if not v.is_valid(instance):
            if quiet:
                # IF HAVE TO PRINT ERROR MESSAGE, PRINT INTRO TOO
                print(f"instance = {filename}")
            else:
                print("")
            for error in sorted(v.iter_errors(instance), key=str):
                print("\t\t", end="")
                for elem in error.path:
                    print(f"['{elem}']", end="")
                print(f": {error.message}")
            print("\tFAILED")
            return False
        else:
            if not quiet:
                print("OK")
            return True
    except jsonschema.ValidationError as e:
        if quiet:
            # IF HAVE TO PRINT ERROR MESSAGE, PRINT INTRO TOO
            print(f"instance = {filename}")
        else:
            print("")
        print("\t" + e.message)
        return False


def get_information_file_format(filename):
    """
    Determines if the information file is in JSON or YAML format

    Assumes that the filename is "*.{FORMAT}
    """

    format = filename.split(".")[-1].upper()
    if format in VALID_FORMATS:
        return format
    print("Unknown format: {format}")
    sys.exit(1)


def _read_json_yaml(filename, format=None, debug=False):
    """ Reads a JSON or YAML file.  Does NOT use jsonReference """
    if not format:
        format = get_information_file_format(filename)

    with open(filename, "r") as f:
        if format == "YAML":
            try:
                element = yaml.safe_load(f)
            except Exception:
                print(f"Error loading YAML file: {filename}")
                print(sys.exc_info()[1])
                return
        else:
            try:
                element = json.load(f)
            except json.decoder.JSONDecodeError as e:
                print(f"JSONDecodeError: Error loading JSON file: {filename}")
                print(str(e))
                return
            except Exception:
                print(f"Error loading JSON file: {filename}")
                print(sys.exc_info()[1])
                return

    return element


def _read_json_yaml_ref(filename, format=None, debug=False):
    """ Reads a JSON or YAML file using jsonReference """
    if not format:
        format = get_information_file_format(filename)

    base_path = Path(filename).resolve().parent
    base_uri = f"file:{base_path}/"
    # print(f'read_json_yaml_ref: base_uri={base_uri}')
    with open(filename, "r") as f:
        return yamlref_load(f, base_uri=base_uri)


def read_info_file(filename, format=None):
    """
    Reads an information file
    """
    # A = InfoDict(_read_json_yaml_ref(filename, format))
    # A.propagate()  # Makes all subdicts InfoDicts
    A = _read_json_yaml_ref(filename, format)
    return A


def _validate_script(argv=None):
    """
    Validate an information file

    Validates a file named *.{TYPE}.json or *.{TYPE}.yaml against the
     schema.{TYPE}.json file.

    {TYPE} can be campaign, network, instrumentation, instrument_components or
    response
    """
    from argparse import ArgumentParser

    parser = ArgumentParser(prog="campaign_validate", description=__doc__)
    parser.add_argument("info_file", help="Information file")
    parser.add_argument("-t", "--type",
                        choices=VALID_TYPES,
                        default=None,
                        help="Forces information file type (overrides "
                             "interpreting from filename)")
    parser.add_argument("-f", "--format", choices=VALID_FORMATS,
                        default=None,
                        help="Forces information file format (overrides "
                             "interpreting from filename)")
    parser.add_argument("-s", "--schema", default=None,
                        help="Schema file (overrides interpreting from "
                             "filename)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output verbosity")
    args = parser.parse_args()

    validate(args.info_file, format=args.format, type=args.type,
             schema_file=args.schema, verbose=args.verbose)
