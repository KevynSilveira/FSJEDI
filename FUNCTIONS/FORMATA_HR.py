def format_time(seconds): # Formata o texto para DD:HH:MM:SS
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}"