import os, re

class Res:
    def __init__(self, name, base_dir=r"C:\eBEST\xingAPI\Res"):
        self.name = name
        self.path = os.path.join(base_dir, self.name+'.res')
        self.blocks = self.parse_res(self.path)

    def __call__(self, block_name):
        return self.get(block_name)

    def get(self, block_name):
        block_name = block_name.lower()
        if self.name.lower() in block_name:
            block_name = block_name.replace(self.name.lower(), '')
        for key in self.blocks.keys():
            if block_name in key.lower():
                block_name = key
        block_codes = self.blocks[block_name]
        return block_name, block_codes

    @staticmethod    
    def parse_res(path):
        with open(path, encoding="euc-kr") as f:
            read    = f.read().replace('\t', '')
            data    = re.search(r"BEGIN_DATA_MAP([\S\s]*)END_DATA_MAP", read)
            blocks  = re.findall(r"([\S\s]*?)\sbegin\s([\S\s]*?)\send\s", data.group(1))

        parsed_blocks = {}
        for block in blocks:
            block_name  = re.sub(' |\n', '', block[0]).split(',')[0]
            block_codes = {}
            for block_item in list(filter(None, re.sub(' |\n', '', block[1]).split(';'))):
                code_name, code_key = block_item.split(',')[:2]
                block_codes[code_key] = code_name
            parsed_blocks[block_name] = block_codes

        return parsed_blocks
