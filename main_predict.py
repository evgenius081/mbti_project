import os.path

from BERT.predict import predict_for_texts


def check(str_to_check, expected_result):
    index = 0
    for i in range(len(expected_result)):
        if expected_result[i] == str_to_check[i]:
            index += 1
    return index

def get_progress():
    progress_file = open("../BERT/data/progress.txt", "r", encoding="UTF8")
    percentage = [0, 0, 0, 0, 0]
    count = 0
    for line in progress_file:
        count += 1
        percentage[int(line.replace("\n", ""))] += 1
    progress_file.close()
    return count, percentage

def main():
    with open("../BERT/data/tests_test.txt", "r", encoding="utf8") as test_file:
        with open("../BERT/data/progress.txt", "a", encoding="utf8") as progress_file:
            (already_count, percentage) = get_progress()
            count = 0
            prev_percent = 0
            for line in test_file:
                if count < already_count:
                    count += 1
                    continue
                try:
                    parts = line.split("|")
                    expected = parts[1]
                    result = predict_for_texts(parts[2].replace("\n", ""))
                    count += 1
                    index = check(result, expected)
                    progress_file.write(f"{index}\n")
                    percentage[index] += 1
                    if prev_percent < int(count * 100 / 102496):
                        prev_percent = int(count * 100 / 102496)
                        print(f"{prev_percent}%")
                except Exception:
                    pass
            return count, percentage

(count_sum, percentages) = main()

for part in percentages:
    print(f"{round(part/count_sum * 100, 2)}%")