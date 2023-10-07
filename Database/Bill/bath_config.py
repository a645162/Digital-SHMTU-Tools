# # 1为保留最新记录，0为保留最早记录！(还未实现)
# order = 0

# 最大间隔时间
# 如果多个连续记录且间隔均小于这个间隔，那么将被认定为一条记录
# 不可以超过120分钟，若设定超过120分钟则自动设定为120分钟
max_interval_minute = 30


def get_max_interval_seconds():
    global max_interval_minute
    if max_interval_minute > 120:
        max_interval_minute = 120
    return max_interval_minute * 60


if __name__ == '__main__':
    print(get_max_interval_seconds())
