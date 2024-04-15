from src import (
    arguments,
    utils,
    cfg_reader,
    unit_testing,
    metrics,
    interfacing,
    benchmark_tests,
)


def main():
    args = arguments.parse()
    cfg = cfg_reader.primary.load(args.config)
    
    if args.procedure == 'bigram':
        # run through unit tests
        pass
        
    else:
        raise NotImplementedError(utils.strings.clean_multiline(
            """
            Procedure added to args but case not added to main function in <project root>/lm_toolkit/__init__.py.
            """
        ))
            
