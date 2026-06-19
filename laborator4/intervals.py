def merge_intervals(intervals):
    if not intervals:
        return []
    
    # sortam intervalele dupa punctul de pornire
    sorted_invs = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_invs[0]]
    
    for current in sorted_invs[1:]:
        prev_start, prev_end = merged[-1]
        curr_start, curr_end = current
        
        if curr_start <= prev_end + 1:
            merged[-1] = (prev_start, max(prev_end, curr_end))
        else:
            merged.append(current)
            
    return merged
