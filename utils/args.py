from argparse import ArgumentParser


class UserArgsParser(ArgumentParser):
    def __init__(self, arg_specs: dict, description=None):
        super(UserArgsParser, self).__init__(description)
        # self.arg_parser = ArgumentParser(description=description)
        self._add_args(arg_specs)

    def _add_args(self, arg_specs):
        if arg_specs is None:
            return

        for key in arg_specs:
            if '/' in key:
                flag, f = key.split('/')
                self.add_argument(flag, f, **arg_specs[key])
                continue
            self.add_argument(key, **arg_specs[key])
        return

    def parse_args(self, user_args=None, neglect_dict: dict = None):
        if user_args is not None:
            user_args = [a.strip() for a in user_args.split(' ') if a.strip() != '']
        # user_args = self.parse_args(user_args)
        user_args, unknown_args = self.parse_known_args(user_args)
        if neglect_dict is not None:
            for key in neglect_dict:
                setattr(user_args, key, neglect_dict[key])
        return user_args
