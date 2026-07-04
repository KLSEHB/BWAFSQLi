import random


def save_to_file(data, filename):
    with open(filename, 'w') as f:
        for line in data:
            f.write(line)


def split_data(input_file, train_file, val_file, test_file, split_ratio=(0.6, 0.2, 0.2), shuffle=True):
    if sum(split_ratio) != 1:
        raise ValueError("Split ratio must sum to 1.")

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = list(set(f.readlines()))
    except Exception as e:
        print(f"Error reading input file: {e}")
        return

    if shuffle:
        random.shuffle(lines)

    total_samples = len(lines)
    train_size = int(split_ratio[0] * total_samples)
    val_size = int(split_ratio[1] * total_samples)
    test_size = total_samples - train_size - val_size

    train_set = lines[:train_size]
    val_set = lines[train_size:train_size + val_size]
    test_set = lines[train_size + val_size:]

    try:
        save_to_file(train_set, train_file)
        save_to_file(val_set, val_file)
        save_to_file(test_set, test_file)
    except Exception as e:
        print(f"Error writing to file: {e}")
        return

    print(f"Data split and saved successfully:")
    print(f"Training set: {train_file} ({len(train_set)} samples)")
    print(f"Validation set: {val_file} ({len(val_set)} samples)")
    print(f"Test set: {test_file} ({len(test_set)} samples)")

split_data("CFG-D/sqli.txt", "CFG-D/sqli_train.txt", "CFG-D/sqli_val.txt", "CFG-D/sqli_test.txt")

