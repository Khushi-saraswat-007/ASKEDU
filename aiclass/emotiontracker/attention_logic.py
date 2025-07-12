def check_attention(avg_ear, threshold=0.25):
    if avg_ear < threshold:
        return "Not Attentive", (0, 0, 255)
    else:
        return "Attentive", (0, 255, 0)
