from .pretty_printer import pretty_print


def print_driver_df(name, df):
    pretty_print(f"\n[+] {name}:")
    pretty_print(df)
