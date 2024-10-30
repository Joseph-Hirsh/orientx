from .pretty_printer import pretty_print
from .. import config


def print_driver_df(name, df):
    pretty_print(f"\n[+] {name}:")
    pretty_print(df)


def print_parameters(args):
    if not config.QUIET:
        pretty_print("Parameters: ")
        for arg in vars(args):
            pretty_print(f"    {arg}: {getattr(args, arg)}")
        pretty_print("\n")
    else:
        pretty_print("Running in quiet mode...")


def print_argument_error(error):
    pretty_print(f"[!] {error}")

