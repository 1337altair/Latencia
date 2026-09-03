def score_connection(ping, jitter, loss):
    score = 100.0

    if ping > 20:
        score -= min((ping - 20) * 0.22, 30)
    if jitter > 5:
        score -= min((jitter - 5) * 0.7, 25)

    score -= min(loss * 8, 40)
    return max(0, min(100, round(score)))
