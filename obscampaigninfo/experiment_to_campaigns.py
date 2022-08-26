from argparse import ArgumentParser
import json
import copy
from collections import OrderedDict

import yaml

from .info_files import validate, read_info_file, get_information_file_format


def main():
    """
    Convert an experiment file to several campaign files
    """
    parser = ArgumentParser(prog="experiment_to_campaigns",
                            description=__doc__)
    parser.add_argument("expt_file", help="Experiment file")
    args = parser.parse_args()
    _experiment_to_campaigns(args.expt_file)
    
def _experiment_to_campaigns(fname, quiet=False):
    format = get_information_file_format(fname)
    assert format in ['JSON', 'YAML']
    validate(fname, type='experiment', quiet=quiet)

    A = dict(read_info_file(fname))

    exp_name = A['experiment']['reference_name']
    fdsn_name = A['experiment']['fdsn_network']['name']
    if not  exp_name == fdsn_name:
        print('Experiment reference_name != FDSN network name ("{}" != "{}")'
          .format(exp_name, fdsn_name))
        print('Going ahead, but make sure you wanted to do this!'
          .format(exp_name, fdsn_name))

    expedition_details = A['experiment'].pop('expeditions', {})
    campaigns = A['experiment'].pop('campaigns')
    root = dict(A)
    root['campaign'] = root.pop('experiment')
    
    for key, campaign in campaigns.items():
        B = copy.deepcopy(root)
        C = B['campaign']
        B['experiment'] = {'reference_name': exp_name,
                           'start_date': B.get('start_date',
                                               C['fdsn_network']['start_date']),
                           'end_date': B.get('end_date',
                                             C['fdsn_network']['end_date'])
                           }
        C.update(campaign)
        C['reference_name'] = key
        if 'expeditions' in C:
            for v in C['expeditions']:
                if v['name'] in expedition_details:
                    v.update(expedition_details[v['name']])
                else:
                    print('"{}" not found in "expeditions", ignored'
                          .format(v["name"]))
        # Sort the dictionary to desired order
        D = {k: B[k] for k in ['format_version','revision','experiment','campaign']}
        if format == 'JSON':
            out_file = f'{C["reference_name"]}.campaign.json'
            out_func = json.dump
        else:
            out_file = f'{C["reference_name"]}.campaign.yaml'
            out_func = yaml.dump
        if not quiet:
            print(f'Writing to {out_file}, {format} format')
        with open(out_file, 'w') as fp:
            out_func(D, fp, sort_keys=False)
