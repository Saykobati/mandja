import re

def isint(value):
    """ Check if 'value' is integer """
    
    result = True
    try:
        num = int(value)
    except (ValueError, TypeError):
        result = False
        
    return result


def isip4addr(ip_str):
    if not isinstance(ip_str, str):
        return False
    
    pattern = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"\
              r"\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"\
              r"\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"\
              r"\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    
    if re.match(pattern, ip_str):
        return True
    else:
        return False