def calculate_jitter(samples):
    if len(samples) < 2:
        return 0.0

    differences = [
        abs(samples[index] - samples[index - 1])
        for index in range(1, len(samples))
    ]

    return sum(differences) / len(differences)
