import random
import re


def convert_case(text, to_upper=False):
    return text.upper() if to_upper else text.lower()


def remove_comments(text):
    text = re.sub(r'#.*', '# ', text)
    text = re.sub(r'--.*', '-- ', text)
    text = re.sub(r'--+.*', '--+', text)
    text = re.sub(r'/\*.*?\*/', ' ', text, flags=re.DOTALL)
    return text


def replace_control_chars(text):
    control_map = {
        '\n': ' ',
        '\t': ' ',
        '\r': ' ',
        '\v': ' ',
        '\f': ' ',
    }
    for char, rep in control_map.items():
        text = text.replace(char, rep)
    return text


def DML_substitute(text):
    control_map = {
        '||': 'or',
        '&&': 'and',
        'like': '=',
    }
    for char, rep in control_map.items():
        text = text.replace(char, rep)
    return text


def convert_hex_in_int(input_string):
    match = re.match(r'^(-?0x[0-9A-Fa-f]+)', input_string)

    if match:
        hex_num = match.group(1)
        decimal_value = int(hex_num, 16)
        input_string = input_string.replace(hex_num, str(decimal_value), 1)
    return input_string


def convert_hex_to_char(text):
    def hex_to_string(hex_string):
        if hex_string.startswith('='):
            hex_string = hex_string[1:].strip()
        if hex_string.startswith('0x'):
            hex_string = hex_string[2:]
        bytes_object = bytes.fromhex(hex_string)
        return bytes_object.decode("utf-8", errors='ignore')

    hex_parts = re.findall(r'= ?0x[0-9A-Fa-f]+', text)

    decoded_text = text
    for hex_part in hex_parts:
        quote = random.choice(["'", '"'])
        decoded_subtext = "=" + quote + hex_to_string(hex_part) + quote
        decoded_text = decoded_text.replace(hex_part, decoded_subtext)

    return decoded_text


def collapse_spaces(text):
    return re.sub(r'\s+', ' ', text)


def replace_inline(text):
    return re.sub(r'/\*!\s*(.*?)\s*\*/', r'\1', text)


def defend_process(text):
    origin_text = text
    try:
        text = convert_case(text)
        text = collapse_spaces(text)

        text = replace_inline(text)
        text = remove_comments(text)
        text = replace_control_chars(text)
        text = DML_substitute(text)
        text = convert_hex_in_int(text)
        text = convert_hex_to_char(text)

        text = convert_case(text)
        text = collapse_spaces(text)
        return text
    except Exception as e:
        print(f"Error during processing: {e}")
        return origin_text


if __name__ == "__main__":
    text = "1'\r/*!or*/\r1=1--+warships remainder"
    print(defend_process(text))
