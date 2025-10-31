TEMP = 25

def get_diff_from_comfortable_temp(*, temperature: int) -> int:
    return TEMP - temperature


print(get_diff_from_comfortable_temp(temperature=20))