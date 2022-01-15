def time_elapsed_str(timeDelta):
    timeDelta = abs(timeDelta)
    if timeDelta.days > 0:
        if timeDelta.days == 1:
            return '1 day ago'
        else:
            return '%s days ago' % timeDelta.days
    elif timeDelta.seconds / 3600 > 0:
        if timeDelta.seconds / 3600 == 1:
            return '1 hour ago'
        else:
            return '%s hours ago' % round(timeDelta.seconds / 3600, 1)
    elif timeDelta.seconds / 60 < 2:
        return '1 minute ago'
    else:
        return '%s minutes ago' % round((timeDelta.seconds / 60), 1)