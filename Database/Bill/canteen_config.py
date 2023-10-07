import datetime


def parse_date_str(date_str):
    date_str = str(date_str)
    date_str_list = date_str.split(".")
    if len(date_str_list) == 3:
        return int(date_str_list[0]), int(date_str_list[1]), int(date_str_list[2])
    else:
        return None, None, None


def compare_date(date1, date2):
    date1 = str(date1)
    date2 = str(date2)

    date1_turple = parse_date_str(date1)
    date2_turple = parse_date_str(date2)

    if date1_turple[0] > date2_turple[0]:
        return 1
    elif date1_turple[0] < date2_turple[0]:
        return 2
    else:
        # year is equal
        if date1_turple[1] > date2_turple[1]:
            return 1
        elif date1_turple[1] < date2_turple[1]:
            return 2
        else:
            # year and month is equal
            if date1_turple[2] > date2_turple[2]:
                return 1
            elif date1_turple[2] < date2_turple[2]:
                return 2
            else:
                return 0


def date_is_in_range(date, start_date, end_date):
    date = str(date).strip()
    start_date = str(start_date).strip()
    end_date = str(end_date).strip()
    if end_date == "now":
        now = datetime.datetime.now()
        end_date = "{}.{}.{}".format(now.year, now.month, now.day)
    return compare_date(date, start_date) != 2 and compare_date(date, end_date) != 1


def parse_time_str(time_str):
    time_str = str(time_str)
    time_str_list = time_str.split(":")
    if len(time_str_list) == 3:
        return int(time_str_list[0]), int(time_str_list[1]), int(time_str_list[2])
    elif len(time_str_list) == 2:
        return int(time_str_list[0]), int(time_str_list[1]), 0
    else:
        return None, None, None


def compare_time(time1, time2):
    time1 = str(time1)
    time2 = str(time2)

    time1_turple = parse_time_str(time1)
    time2_turple = parse_time_str(time2)

    if time1_turple[0] > time2_turple[0]:
        return 1
    elif time1_turple[0] < time2_turple[0]:
        return 2
    else:
        # year is equal
        if time1_turple[1] > time2_turple[1]:
            return 1
        elif time1_turple[1] < time2_turple[1]:
            return 2
        else:
            # year and month is equal
            if time1_turple[2] > time2_turple[2]:
                return 1
            elif time1_turple[2] < time2_turple[2]:
                return 2
            else:
                return 0


def time_is_in_range(time, start_time, end_time):
    time = str(time).strip()
    start_time = str(start_time).strip()
    end_time = str(end_time).strip()
    return compare_time(time, start_time) != 2 and compare_time(time, end_time) != 1
