from keyflow import kfprint

def logtext(text):
    return kfprint(f"{text}\n", speed=0.01, fore_color='green', bold=True)