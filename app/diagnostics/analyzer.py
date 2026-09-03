from app.i18n.language import t


def quality(value, good, fair, reverse=False):
    if value is None:
        return "unknown"

    if reverse:
        if value <= good:
            return "good"
        if value <= fair:
            return "fair"
        return "bad"

    if value >= good:
        return "good"
    if value >= fair:
        return "fair"
    return "bad"


def analyze(result, network, gateway, dns, internet):
    ping = result["ping"]
    jitter = result["jitter"]
    loss = result["packet_loss"]
    gateway_ping = gateway.get("latency")

    issues = []

    if not internet.get("online"):
        issues.append(t("diag_no_internet"))
    else:
        if gateway_ping is not None and gateway_ping >= 30:
            issues.append(t("diag_local_problem"))

        if gateway_ping is not None and gateway_ping < 15 and ping >= 80:
            issues.append(t("diag_external_problem"))

        if loss >= 5:
            issues.append(t("high_loss"))
        elif loss > 0:
            issues.append(t("small_loss"))

        if jitter >= 30:
            issues.append(t("high_jitter"))
        elif jitter >= 15:
            issues.append(t("mid_jitter"))

        if ping >= 100:
            issues.append(t("high_ping"))
        elif ping >= 50:
            issues.append(t("mid_ping"))

        if dns is None:
            issues.append(t("diag_dns_failed"))
        elif dns >= 150:
            issues.append(t("diag_dns_slow"))

    if not issues:
        issues.append(t("all_good"))

    score = 100
    score -= min(loss * 8, 40)
    score -= min(max(ping - 20, 0) * 0.18, 25)
    score -= min(max(jitter - 5, 0) * 0.55, 20)

    if gateway_ping is not None:
        score -= min(max(gateway_ping - 5, 0) * 0.35, 15)

    if dns is not None:
        score -= min(max(dns - 60, 0) * 0.05, 10)

    if not internet.get("online"):
        score = 0

    score = max(0, min(100, round(score)))

    if score >= 90:
        health = "excellent"
    elif score >= 75:
        health = "good"
    elif score >= 55:
        health = "fair"
    else:
        health = "poor"

    return {
        "score": score,
        "health": health,
        "issues": issues,
        "metrics": {
            "internet": "online" if internet.get("online") else "offline",
            "gateway": gateway.get("gateway") or "-",
            "gateway_ping": gateway_ping,
            "ping": ping,
            "jitter": jitter,
            "packet_loss": loss,
            "dns": dns,
            "local_ip": network.get("local_ip", "-"),
            "adapter": network.get("adapter", "-")
        }
    }
