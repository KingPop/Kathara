import argparse

from ... import utils
from ...foundation.cli.command.Command import Command
from ...manager.ManagerProxy import ManagerProxy
from ...strings import strings, wiki_description
from ...trdparty.curses.curses import Curses


class ListCommand(Command):
    def __init__(self):
        Command.__init__(self)

        parser = argparse.ArgumentParser(
            prog='kathara list',
            description=strings['list'],
            epilog=wiki_description,
            add_help=False
        )

        parser.add_argument(
            '-h', '--help',
            action='help',
            default=argparse.SUPPRESS,
            help='Show an help message and exit.'
        )

        parser.add_argument(
            '-a', '--all',
            required=False,
            action='store_true',
            help='Show all running Kathara devices of all users. MUST BE ROOT FOR THIS OPTION.'
        )

        parser.add_argument(
            '-l', '--live',
            required=False,
            action='store_true',
            help='Live mode.'
        )

        parser.add_argument(
            '-n', '--name',
            metavar='DEVICE_NAME',
            required=False,
            help='Show only information about a specified device.'
        )

        self.parser = parser

    def run(self, current_path, argv):
        self.parse_args(argv)
        args = self.get_args()

        if args.all and not utils.is_admin():
            raise Exception("You must be root in order to show all Kathara devices of all users.")

        all_users = bool(args.all)

        if args.live:
            if args.name:
                self._get_machine_live_info(args.name, all_users)
            else:
                self._get_lab_live_info(all_users)
        else:
            if args.name:
                print(ManagerProxy.get_instance().get_machine_info(args.name, all_users=all_users))
            else:
                lab_info = ManagerProxy.get_instance().get_lab_info(all_users=all_users)

                print(next(lab_info))

    @staticmethod
    def _get_machine_live_info(machine_name, all_users):
        Curses.get_instance().init_window()

        try:
            while True:
                Curses.get_instance().print_string(
                    ManagerProxy.get_instance().get_machine_info(machine_name, all_users=all_users)
                )
        finally:
            Curses.get_instance().close()

    @staticmethod
    def _get_lab_live_info(all_users):
        lab_info = ManagerProxy.get_instance().get_lab_info(all_users=all_users)

        Curses.get_instance().init_window()

        try:
            while True:
                Curses.get_instance().print_string(next(lab_info))
        except StopIteration:
            pass
        finally:
            Curses.get_instance().close()
