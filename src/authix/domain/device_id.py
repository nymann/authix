import xxhash


def generate_device_id(refresh_token: str):
    return xxhash.xxh3_64_hexdigest(refresh_token)
