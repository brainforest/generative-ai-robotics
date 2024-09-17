def get_raspberry_pi_model():
    model = "Unknown"
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if "Model" in line:
                    model = line.split(":")[-1].strip()
                    break
    except FileNotFoundError:
        model = "Not running on Raspberry Pi"
    
    return model

# Example usage
model = get_raspberry_pi_model()
print("Raspberry Pi Model:", model)

