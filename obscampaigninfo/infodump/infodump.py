"""
Create standardized output file for RESIF Marine A-node

Basé sur fichiers/email envoyé par Olivier Dewee le 26/11/2021
"""
from argparse import ArgumentParser
import json
from pprint import pprint
import copy

import yaml

from ..info_files import validate, read_info_file, get_information_file_format

out_level = 3  # 1 = EXPERIMENT, 2 = CAMPAIGN or 3 = FACILITY


def _infodump_script():
    """
    Run infodump from the command line
    """
    parser = ArgumentParser(prog="infodump_campaign", description=__doc__)
    parser.add_argument("campaign_file", help="Campaign file")
    args = parser.parse_args()
    infodump(args.campaign_file)


def infodump(in_fname, quiet=False):
    """
    Read campaign file and output standardized JSON file:
    Experiment > Campaign > Facility

    Args:
        in_fname (str): campaign file name
        quiet (bool): do not print out any information
    Returns:
        (str): output file name
    """
    format = get_information_file_format(in_fname)
    assert format in ['JSON', 'YAML']
    validate(in_fname, type='campaign', quiet=quiet)
    A = dict(read_info_file(in_fname))
    net_ref = _get_net_ref(A['campaign']['fdsn_network'])

    out_dict = {}
    expt_name, exp_dict = _experiment_dict(A)
    out_dict['experiments'] = [exp_dict]
    out_fbase = expt_name

    if out_level > 1:
        camp_name, camp_dict = _campaign_dict(A, expt_name, net_ref)
        out_dict['campaigns'] = [camp_dict]
        out_fbase += f'.{camp_name}'
    if out_level > 2:
        out_dict['facilities'] = _facilities(A, camp_name, expt_name, net_ref)
        out_fbase += '.facilities'
    out_fname = out_fbase + '.experiment.json'
    with open(out_fname, 'w') as fp:
        json.dump(out_dict, fp, indent=4)
    return out_fname

def _get_net_ref(fdsn_dict):
    start_year = fdsn_dict['start_date'].split('-')[0]
    return f"{fdsn_dict['code']}+{start_year}"

def _experiment_dict(root):
    """
    Returns:
        (tuple):
            refname (str): Experiment reference name
            exp_dict (dict): Experiment dictionary
    """
    in_dict = root['experiment']
    refname = in_dict['reference_name']

    out_dict = {'_experiment_ref': refname,
                'name': refname,
                'working-period': {'start-date': in_dict['start_date'],
                                   'end-date': in_dict['end_date']}}
    return refname, out_dict


def _campaign_dict(root, expt_name, net_ref):
    """
    Args:
        root (dict): read from campaign file
        expt_name (str): experiment name
        net_ref (str): fdsn network reference name

    Returns:
        (tuple):
            refname (str): Campaign reference name
            camp_dict (dict): Campaign dictionary
    """
    in_dict = root['campaign']

    refname = in_dict['reference_name']
    
    out_dict = {}
    out_dict["_campaign_ref"] = f'{refname}@{expt_name}'
    out_dict['name'] = refname
    out_dict['is-associated-to'] = {"_network-ref": net_ref}
    out_dict['scientist'] = {
        "first-name": in_dict['reference_scientist']['first_name'],
        "last-name": in_dict['reference_scientist']['last_name'],
        "email": in_dict['reference_scientist']['email']}

    out_dict["validation-methods"] = {}
    wave_windows = _make_wave_windows(in_dict)
    if wave_windows is not None:
        out_dict["validation-methods"]["BY-WAVEFORM"] =  {"events": wave_windows}
    return refname, out_dict


def _facilities(root, campaign_name, expt_name, net_ref):
    """
    Args:
        root (dict): facility object
        campaign_name (str): campaign name
        expt_name (str): experiment name
        net_ref (str): FDSN network reference name
    Returns:
        (list of dicts)
    """
    in_dict = root['campaign']['operators']
    out_list = []

    for ref_name, op_dict in in_dict.items():
        out_dict = {}
        out_dict['_facility_ref'] = f"{ref_name}@{campaign_name}@{expt_name}"
        out_dict['name'] = ref_name
        if "full_name" in op_dict:
            out_dict['full_name'] = op_dict['full_name']
        out_dict['has-operated'] = {"_station-refs":
            [f"{x}@{net_ref}" for x in op_dict['stations']]}
        out_list.append(out_dict.copy())
    return out_dict


def _make_station_refs(station_list, net_ref):
    """
    Add net_ref to each element of station_list
    """
    return [f"{x}+{net_ref}" for x in station_list]


def _make_wave_windows(in_dict):
    if 'validation_methods' not in in_dict:
        return None
    if 'waveform_windows' not in in_dict['validation_methods']:
        return None

    wave_windows = []
    for win in in_dict['validation_methods']['waveform_windows']:
        a = {'occurence-period': _get_occurence_period_dict(win),
             'title': win['title'],
             'source-position': _get_source_position(win),
             'notes': win.get('notes',[])}
        wave_windows.append(a.copy())
    return wave_windows


def _get_occurence_period_dict(win):
    out_dict = {'start-datetime': win['starttime']}
    if 'duration.s' in win:
        out_dict['duration.s'] = win['duration.s']
    elif 'duration.min' in win:
        out_dict['duration.s'] = 60.*win['duration.min']
    else:
        raise ValueError('neither duration.s nor duration.min found')
    return out_dict

def _get_source_position(win):
    if not 'source_position' in win:
        return None
    sp = win['source_position']
    a = {'source-position': {'lat.deg': sp['lat'],
                             'lon.deg': sp['lon'],
                             'depth.km': sp.get('depth.km', None)}}
    return a
