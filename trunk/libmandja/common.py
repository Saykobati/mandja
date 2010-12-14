import re

def isint( value ):
    """ Check if 'value' is integer """
    
    isint = True
    try:
        num = int(str)
    except ValueError:
        isint = False
    return isint


def isipaddr(ip_str):
    pattern = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"\
              r"\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"\
              r"\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"\
              r"\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    
    if re.match(pattern, ip_str):
        return True
    else:
        return False