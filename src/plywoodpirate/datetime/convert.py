# <> with ❤️ by Micha Grandel - hello@michagrandel.eu
""" Convert time and dates between different formats """

def get_human_readable_time(**kwargs):
    """
    Converts hours, minutes and seconds to a human-readable format
    
    Add up all hours, minutes and seconds given by the keyword arguments.
    Returns a string with a human-readable format.
    
    Keyword arguments:
        hours(int): hours 
        minutes(int): minutes 
        seconds(int): seconds
    
    Returns:
        str: human-readable duration
    """
    hours: int = kwargs.get("hours", 0)
    minutes: int = kwargs.get("minutes", 0)
    seconds: int = kwargs.get("seconds", 0)

    total_seconds: int = hours * 3600 + minutes * 60 + seconds

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = int(total_seconds % 60)

    if hours == 0 and minutes == 0:
        return f"{seconds} seconds"
    elif hours == 0:
        return f"{minutes:02}:{seconds:02} minutes"
    else:
        return f"{hours:02}:{minutes:02}:{seconds:02} hours"
