import csv
from os import listdir
from os.path import isfile, join

from src.record import Record

OUTPUT_PATH = "output/output.csv"
STATION_ID = "BART"


def read_and_filter_csv(csv_path):
    record_list = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            record_list.append(
                Record(row[0], row[1], row[2], row[3], row[4], row[5],
                       row[6], row[7], row[8], row[9], row[10], row[11], row[12]))
        f.close()

    record_list = list(filter(lambda p: STATION_ID == p.station_id, record_list))
    return record_list


def save_to_csv(csv_path, ztd_average_list):
    with open(csv_path, 'w') as file:
        for ztd_average in ztd_average_list:
            for ztd in ztd_average:
                file.write(str(ztd))
                file.write('\n')
    file.close()


def process_file(csv_path_input, record_list):
    single_record_list = read_and_filter_csv(csv_path_input)
    record_list.append(single_record_list)
    return record_list


def count_weight(j):
    return 1 / (j + 2)


def count_average_ztd_edges(record_list, position):
    ztd_average = []
    if position == 0:
        for j in range(0, 6):
            ztd_average.append(record_list[0][j].count_ztd())
    elif position == 1:
        for j in range(0, 6):
            weight_sum = 0
            weight_sum += count_weight(j) + count_weight(j + 6)
            single_ztd = (record_list[1][j].count_ztd() * count_weight(j) +
                          record_list[0][j + 6].count_ztd() * count_weight(j + 6)) / weight_sum
            ztd_average.append(single_ztd)
    elif position == 2:
        for j in range(0, 6):
            weight_sum = 0
            weight_sum += count_weight(j) + count_weight(j + 6) + count_weight(j + 12)
            single_ztd = (record_list[2][j].count_ztd() * count_weight(j) +
                          record_list[1][j + 6].count_ztd() * count_weight(j + 6) +
                          record_list[0][j + 12].count_ztd() * count_weight(j + 12)) / weight_sum
            ztd_average.append(single_ztd)
    print("ZTD list (edge): " + str(ztd_average))  # debug; todo delete
    return ztd_average


def count_average_ztd(record_list):
    ztd_average = []
    for j in range(0, 6):
        weight_sum = 0
        weight_sum += count_weight(j) + count_weight(j + 6) + count_weight(j + 12) + count_weight(j + 18)
        single_ztd = (record_list[3][j].count_ztd() * count_weight(j) +
                      record_list[2][j + 6].count_ztd() * count_weight(j + 6) +
                      record_list[1][j + 12].count_ztd() * count_weight(j + 12) +
                      record_list[0][j + 18].count_ztd() * count_weight(j + 18)) / weight_sum
        ztd_average.append(single_ztd)
    print("ZTD list: " + str(ztd_average))  # debug; todo delete
    return ztd_average


def count_average_ztd_last_files(record_list):
    ztd_last_files = []
    for i in range(0, 3):
        record_list.pop(0)
        ztd_last_files.append(count_average_ztd_edges(record_list, 2 - i))
    return ztd_last_files


def process_files_in_directory(directory_path):
    files = [file for file in listdir(directory_path) if isfile(join(directory_path, file))]
    files.sort()
    position = 0
    record_list = []
    ztd_average_list = []
    for file in files:
        if file != ".DS_Store":
            print(file)
            record_list = process_file(directory_path + "/" + file, record_list)
            if position >= 3:
                if position != 3:
                    record_list.pop(position - 5)
                ztd_average_list.append(count_average_ztd(record_list))
            else:
                ztd_average_list.append(count_average_ztd_edges(record_list, position))
            print(record_list.__len__())  # debug; todo delete
            position += 1
    ztd_average_list.extend(count_average_ztd_last_files(record_list))
    save_to_csv(OUTPUT_PATH, ztd_average_list)


def main():
    process_files_in_directory("data")


if __name__ == '__main__':
    main()
