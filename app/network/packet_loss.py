def calculate_packet_loss(sent, received):
    if sent <= 0:
        return 0.0

    lost = max(sent - received, 0)
    return (lost / sent) * 100
