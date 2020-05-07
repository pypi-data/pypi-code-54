# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neatbio', 'neatbio.alignments', 'neatbio.sequtils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'neatbio',
    'version': '0.0.2',
    'description': 'NeatBio - a simple Yet Another BioInformatics Library for DNA Sequence',
    'long_description': '### neatbio\nA Simple Yet Another Bioinformatics Library for DNA,RNA and Protein Sequencing\n\n### Installation\n```bash\npip install neatbio\n```\n\n### Benefits\n+ Handling Sequences(DNA,RNA,Protein)\n+ Protein Synthesis\n+ Sequence Similarity\n+ Kmers Generation and Kmer Distance\n+ Probable Back Translation of Amino Acids\n+ Reading FASTA files\n\n### Why NeatBio?\n+ NeatBio is yet another bioinformatics library along side powerful and popular bioinformatics libraries such as biopython,scikit-bio,biotite.\n+ It is meant to complement these powerful library in a simple way.\n\n\n### Usage\n#### Handling Sequences\n+ Neatbio offers the ability to analyse sequences for more insight\n\n```python\n>>>import neatbio as nt\n>>> seq1 = nt.Sequence(\'ATGCATTGA\')\n>>> seq1.gc\n33.33333333333333\n>>> seq1.gc_frequency()\n3\n>>> seq1.at\n66.66666666666666\n>>> seq1.at_frequency()\n6\n>>> seq1.transcribe()\n\'AUGCAUUGA\'\n>>> mrna = seq1.transcribe()\n>>> nt.Sequence(mrna).back_transcribe()\n\'ATGCATTGA\'\n>>> \n\n>>> seq1.translate()\n\'MH*\'\n>>> seq1.translate\n>>>\n>>> rna_seq = nt.Sequence("AUGCAUUGA","RNA")\n>>> rna_seq.seqtype\n>>> Sequence(seq=\'AUGCAUUGA\',seqtype=\'RNA\')\n\n```\n\n#### Working with Proteins\n```python\n>>> protein1 = nt.ProteinSeq(\'MIT\')\n>>> protein1\nProteinSeq(seq=\'MIT\')\n>>> protein1.back_translate()\n\'ATGATAACT\'\n\n```\n+ Note that the back_translate() function offers a probable sequence and not the exact\nback-translation as multiple codons can represent the same amino acids.\n\n#### Convert 3 Letter Amino Acid to 1 and vice versa\n```python\n>>> from neatbio.sequtils import convert_3to1,convert_1to3,get_acid_name\n>>> convert_3to1(\'Ala\')\n\'A\'\n>>> convert_1to3(\'L\')\n\'Leu\'\n\n>>> get_acid_name(\'Ala\')\n\'Alanine\'\n```\n\n#### Generate DotPlot\n```python\n>>> import neatbio as nt \n>>> import neatbio.sequtils as utils\n>>> seq1 = nt.Sequence(\'AGTCGTACT\')\n>>> seq2 = nt.Sequence(\'AGGCGCACT\')\n>>> \n>>> utils.dotplot(seq1,seq2)\n |AGGCGCACT\n-----------\nA|■     ■  \nG| ■■ ■    \nT|        ■\nC|   ■ ■ ■ \nG| ■■ ■    \nT|        ■\nA|■     ■  \nC|   ■ ■ ■ \nT|        ■\n>>> \n\n```\n\n#### Reading FASTA Files\n```python\n>>> import neatbio as nt \n>>> file1 = nt.read_fasta(\'sequence.fasta\')\n>>> file1[\'seqRecord\']\n\n\n>>> seq1 = nt.Sequence(file1[\'seqRecord\'])\n```\n\n\n#### Documentation\n+ Please read the [documentation](https://github.com/Jcharis/neatbio/wiki) for more information on what neatbio does and how to use is for your needs.\n\n#### More Features To Add\n+ sequence alignment\n+ writing FASTA files\n+ support for more file formats\n\n\n\n#### Acknowledgements\n   + Inspired by packages like BioPython,Scikit-Bio and Biotite\n\n### NB\n+ Contributions Are Welcomed\n+ Notice a bug, please let us know.\n+ Thanks A lot\n\n### By\n+ Jesse E.Agbe(JCharis)\n+ Jesus Saves @JCharisTech\n',
    'author': 'Jesse E.Agbe(JCharis)',
    'author_email': 'jcharistech@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jcharis/neatbio',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.3,<4.0',
}


setup(**setup_kwargs)
