import getopt


class CommandLineParser:
    def __init__(self):
        self.opts = None
        self.args = None
        self.parsed_args = {}

    def parse_arguments(self, input_args):
        if '-k' not in input_args:
            raise Exception('You have to provide keystore path!')
        if '-p' not in input_args:
            raise Exception('You have to provide password to keystore!')
        self.opts, self.args = getopt.getopt(input_args, "p:k:")
        self.parsed_args = {}
        for opt, val in self.opts:
            if opt == '-p':
                self.parsed_args['password'] = val
            if opt == '-k':
                self.parsed_args['keystore_path'] = val
        return self.parsed_args
