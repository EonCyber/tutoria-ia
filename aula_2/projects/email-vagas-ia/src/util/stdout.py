from keyflow import kfprint
"""
This module provides functions to print styled text to the console.
It uses the `kfprint` function from the `keyflow` library to format the output.
"""
def logtext(text):
    return kfprint(f"{text}\n", speed=0.01, fore_color='green', bold=True)

def loginputtext(text):
    return kfprint(f"{text}\n", speed=0.00, fore_color='yellow', bold=True)

def logaianswer(text):
    return kfprint(f"{text}\n", speed=0.00, fore_color='cyan', bold=False)