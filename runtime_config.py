class RuntimeConfig(object):
    def __init__(self, argv):
        from argparse import ArgumentParser
        parser = ArgumentParser(
            description = 'COVID19 Data Visualization')
        parser.add_argument(
            '-d', '--data-root',
            help = 'The path to the root COVID19 data directory')
        parser.add_argument(
            '-p', '--port',
            type = int,
            default = 8090,
            help = 'The port from which the application should be served')
        parser.add_argument(
            '--debug',
            type = bool,
            default = False,
            help = 'Debug the application')
            
        self.args = vars(parser.parse_args(argv[1:]))
