import json
from typing import List, Tuple

from tqdm import tqdm

from tokenizer_tools.conllz.sentence import SentenceX

Block = List[Tuple[int, str]]


def block_generator(conllx_string: str) -> Block:
    lines = conllx_string.splitlines()

    block = []
    for line_num, line_str in enumerate(lines, start=1):
        if not line_str:  # empty line
            yield block

            # reset
            block = []

            # skip this line
            continue

        block.append((line_num, line_str))

    # last block
    if block:
        yield block


def load_conllx(conllx_string: str) -> List[SentenceX]:
    blocks = block_generator(conllx_string)
    return [parse_block_to_sentence(block) for block in tqdm(list(blocks))]


def parse_block_to_sentence(block: Block) -> SentenceX:
    sentence = SentenceX()
    for index, (line_num, raw_line) in enumerate(block):
        if index == 0:
            meta_string = raw_line.strip("#\t\n ")
            try:
                meta_data = json.loads(meta_string)
            except json.decoder.JSONDecodeError as e:
                raise ValueError("{}. At line {}: {}".format(e, line_num, raw_line))

            sentence.id = meta_data.pop("id")
            sentence.meta = meta_data

            continue  # read head is done

        # line = raw_line.strip()
        item = raw_line.split("\t")

        if not raw_line or not item:
            # skip
            continue

        sentence.write_as_row(item)

    return sentence


def read_conllx(input_fd):
    sentence_list = []

    content = input_fd.read()

    for sentence in load_conllx(content):
        sentence_list.append(sentence)

    return sentence_list


read_conllx_from_string = load_conllx
