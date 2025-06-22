from keyflow import kfprint

def logtext(text):
    return kfprint(f"{text}\n", speed=0.01, fore_color='green', bold=True)

def loginputtext(text):
    return kfprint(f"{text}\n", speed=0.00, fore_color='yellow', bold=True)

def logaianswer(text):
    return kfprint(f"{text}\n", speed=0.00, fore_color='cyan', bold=False)