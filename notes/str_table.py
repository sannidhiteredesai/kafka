import re

data = """
GROUP                          TOPIC                          PARTITION  NEW-OFFSET
some_consumer_group            json-topic                     0          0
some_consumer_group            json-topic                     2          0
some_consumer_group            json-topic                     1          0
"""


def pipe_delimited(line):
    return  '| ' + ' | '.join(line.split()) + ' |'

def convert(str_lines):
    non_empty_lines = [re.sub(' +', ' ', line) for line in str_lines.split('\n') if line]
    # TODO - some error cases check like non_empty_lines=[] ...

    total_columns = len(non_empty_lines[0].split())
    header = pipe_delimited(non_empty_lines[0])
    second_line = '|' + ' - |' * total_columns
    print(header)
    print(second_line)

    for l in non_empty_lines[1:]:
        print(pipe_delimited(l))


convert(data)

"""
Expected output:
| GROUP | TOPIC | PARTITION | NEW-OFFSET |
| - | - | - | - |
| some_consumer_group | json-topic | 0 | 0 |
| some_consumer_group | json-topic | 2 | 0 |
| some_consumer_group | json-topic | 1 | 0 |
"""
