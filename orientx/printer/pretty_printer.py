import re
import pandas as pd
from orientx.config import Styles


def pretty_print(data):
    if isinstance(data, pd.DataFrame):
        print(data)
    elif isinstance(data, str):
        string = data
        string = string.replace("[+]", f"{Styles.GREEN}[+]{Styles.RESET}")
        string = string.replace("[-]", f"{Styles.YELLOW}[-]{Styles.RESET}")
        string = string.replace("[!]", f"{Styles.RED}[!]{Styles.RESET}")
        string = re.sub(r"\[i\](.*?)(\n|$)", rf"{Styles.BOLD}[i]\1{Styles.RESET}\2", string)
        print(string)
    else:
        pretty_print("[!] Unsupported type for pretty_print")
