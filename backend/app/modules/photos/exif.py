def exif_number(value: object) -> float | None:
    try:
        return float(value.numerator / value.denominator)  # type: ignore[attr-defined]
    except (AttributeError, ZeroDivisionError, TypeError):
        try:
            return float(value)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            return None


def exif_gps(exif: object) -> tuple[float | None, float | None]:
    try:
        gps = exif.get_ifd(0x8825)  # type: ignore[attr-defined]
    except (AttributeError, KeyError):
        return None, None
    lat_ref = gps.get(1)
    lon_ref = gps.get(3)
    lat = gps.get(2)
    lon = gps.get(4)
    if not lat or not lon:
        return None, None
    lat_values = [exif_number(v) for v in lat]
    lon_values = [exif_number(v) for v in lon]
    if None in lat_values or None in lon_values:
        return None, None
    latitude = lat_values[0] + lat_values[1] / 60 + lat_values[2] / 3600  # type: ignore[operator]
    longitude = lon_values[0] + lon_values[1] / 60 + lon_values[2] / 3600  # type: ignore[operator]
    if lat_ref == "S":
        latitude *= -1
    if lon_ref == "W":
        longitude *= -1
    return latitude, longitude
