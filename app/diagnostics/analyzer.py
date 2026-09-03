from app.i18n.language import t


def analyze(result, network):
    lines = [
        f'{t("adapter")}: {network["adapter"]}',
        f'{t("local_ip")}: {network["local_ip"]}',
        f'{t("ping")}: {result["ping"]:.1f} ms',
        f'{t("jitter")}: {result["jitter"]:.1f} ms',
        f'{t("packet_loss")}: {result["packet_loss"]:.1f}%',
        ""
    ]

    problems = []

    if result["packet_loss"] >= 5:
        problems.append(t("high_loss"))
    elif result["packet_loss"] > 0:
        problems.append(t("small_loss"))

    if result["ping"] >= 100:
        problems.append(t("high_ping"))
    elif result["ping"] >= 50:
        problems.append(t("mid_ping"))

    if result["jitter"] >= 30:
        problems.append(t("high_jitter"))
    elif result["jitter"] >= 15:
        problems.append(t("mid_jitter"))

    if not problems:
        problems.append(t("all_good"))

    lines.extend(problems)
    return "\n".join(lines)
