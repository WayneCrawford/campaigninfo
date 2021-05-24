from argparse import ArgumentParser
import json
import pprint
import copy

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
    pp = pprint.PrettyPrinter(indent=4)
    format = get_information_file_format(fname)
    assert format in ['JSON', 'YAML']
    validate(fname, type='experiment', quiet=quiet)

    A = dict(read_info_file(fname))

    expedition_details = A['experiment'].pop('expeditions', {})
    campaigns = A['experiment'].pop('campaigns')
    root = dict(A)
    root['campaign'] = root.pop('experiment')
    
    for key, campaign in campaigns.items():
        # print('='*60)
        # print(campaign['reference_name'])
        # print('='*60)
        B = copy.deepcopy(root)
        C = B['campaign']
        C.update(campaign)
        C['reference_name'] = key
        # print(B)
        if 'expeditions' in C:
            for v in C['expeditions']:
                if v['name'] in expedition_details:
                    v.update(expedition_details[v['name']])
                else:
                    print('"{}" not found in "expeditions", ignored'
                          .format(v["name"]))
        # print('C=')
        # pp.pprint(C)
        if format == 'JSON':
            with open(f'{C["reference_name"]}.campaign.json', 'w') as fp:
                json.dump(B, fp)
        else:
            with open(f'{C["reference_name"]}.campaign.yaml', 'w') as fp:
                yaml.dump(B, fp)
