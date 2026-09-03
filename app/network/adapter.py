import psutil


def get_adapters():
    stats = psutil.net_if_stats()
    adapters = []

    for name, data in stats.items():
        adapters.append(
            {
                "name": name,
                "up": data.isup,
                "speed": data.speed,
                "mtu": data.mtu,
            }
        )

    return adapters
