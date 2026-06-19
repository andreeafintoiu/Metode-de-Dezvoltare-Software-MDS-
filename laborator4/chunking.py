def chunk(lst, n):
    if n <= 0:
        raise ValueError("n must be positive")
    result = []
    for i in range(0, len(lst), n):
        result.append(lst[i:i + n])
    return result

def flatten(lst_of_lsts):
    result = []
    for sublist in lst_of_lsts:
        result.extend(sublist)
    return result
