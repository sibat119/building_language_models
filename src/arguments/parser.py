import argparse
import argcomplete
from src.utils import files, strings

def parse():
    """
    parse the command line arguments
    """

    ######################### begin arg definitions ######################### 

    # define arguments and parse
    parser = argparse.ArgumentParser() 

    # create subparser for procedures
    subparser = parser.add_subparsers(
        description='decides on which procedure to run',
        required=True,
        dest='procedure',
    )

    # add subparser for playbook generation
    parser_gen = subparser.add_parser(
        'bigram',
        description='generates ansible playbooks'
    )
    
    parser_gen.add_argument(
        '--debug',
        help='used for testing the create_ansible function',
        action='store_true',
        default=False,
    )

    
    ######################### end arg definitions ######################### 

    # parse
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    # perform substitutions
    args.config = strings.replace_slot(
        args.config, 
        { 'PROJECT_ROOT' : files.get_project_root() }
    )

    return args
