import os
import re
import requests
import markovify
import sys
import html2text


fnf = ": error: file not found. please provide a path to a really-existing file!"


def url(insert):
    """ fetch a webpage, return it as html """
    try:
        req = requests.get(insert)
        req.raise_for_status()
        req.encoding = req.apparent_encoding
        # use chardet to catch encoding issue with ISO-8859-1/Latin-1.
    except Exception as exc:
        print(f": there was trouble: {exc}.\n: please enter a valid url.")
        sys.exit()
    else:
        print(": fetched html from url.")
        return req.text


def convert_html(html):
    """ convert a html page to plain text """
    h2t = html2text.HTML2Text()
    h2t.images_to_alt = True
    h2t.ignore_links = True
    h2t.ignore_emphasis = True
    h2t.ignore_tables = True
    h2t.unicode_snob = False
    h2t.decode_errors = "replace"
    h2t.escape_all = False  # remove all noise if needed
    s = h2t.handle(html)
    s = re.sub("[#*]", "", s)  # remove hashes and stars from the 'markdown'
    print(": html converted to plain text")
    return s


def read(infile):
    """ read a file so its ready for markov """
    try:
        if infile.lower().endswith(".pdf"):
            print(
                "looks like you entered a pdf file. you need to use the '-P' flag to convert it."
            )
            sys.exit()
        else:
            with open(infile, encoding="utf-8") as f:
                return f.read()
    except UnicodeDecodeError:
        with open(infile, encoding="latin-1") as f:
            return f.read()
    except IsADirectoryError as exc:
        print(
            f": there was trouble: {exc}.\n: looks like you entered a directory. use '-d' for that."
        )
        sys.exit()
    except FileNotFoundError:
        print(fnf)
        sys.exit()


def mkbtext(texttype, args_ss, args_wf):
    """ build a markov model """
    return markovify.Text(texttype, state_size=args_ss, well_formed=args_wf)


def mkbnewline(texttype, args_ss, args_wf):
    """ build a markov model, newline """
    return markovify.NewlineText(texttype, state_size=args_ss, well_formed=args_wf)


def writeshortsentence(tmodel, args_sen, args_out, args_over, args_len):
    """ actually make the damn litter-atchya, appended to outfile, short sentence """
    output = open(args_out, "a")  # append
    for i in range(args_sen):
        output.write(
            "\n"
            + str(
                tmodel.make_short_sentence(
                    tries=2000, max_overlap_ratio=args_over, max_chars=args_len
                )
            )
            + "\n\n"
        )
    output.write(str("*\n\n"))
    output.close()


def writesentence(tmodel, args_sen, args_out, args_over, args_len):
    """ actually make the damn litter-atchya, appendended to outfile """
    output = open(args_out, "a")  # append
    for i in range(args_sen):
        output.write(
            str(
                tmodel.make_sentence(
                    tries=2000, max_overlap_ratio=args_over, max_chars=args_len
                )
            )
            + "\n\n"
        )
    output.write(str("*\n\n"))
    output.close()


# functions for args.directory:
def dir_list(directory):
    """ returns a list of all text files from a directory"""
    # create a list of files to concatenate:
    matches = []
    if os.path.isdir(directory) is True:
        for root, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith((".txt", ".org", ".md")):
                    matches.append(os.path.join(root, filename))
        print(": text files fetched and combined")
    else:
        print(": error: please enter a valid directory")
        sys.exit()
    return matches


def dir_cat(matchlist, bulkfile):
    """ takes a list of files, returns single concatenated file """
    # concatenate into batchfile.txt:
    with open(bulkfile, "w") as outfile:
        for fname in matchlist:
            try:
                with open(fname, encoding="utf-8") as infile:
                    outfile.write(infile.read())
            except UnicodeDecodeError:
                with open(fname, encoding="latin-1") as infile:
                    outfile.write(infile.read())


# extract full text from a pdf:
def convert_pdf(path):
    try:
        from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
        from pdfminer.converter import TextConverter
        from pdfminer.layout import LAParams
        from pdfminer.pdfpage import PDFPage
        from io import StringIO
    except ModuleNotFoundError as exc:
        print(
            f": there was trouble: {exc}.\n: install 'pdfminer.six' with pip to convert a pdf."
        )
        sys.exit()
    print(": converting pdf file...")
    try:
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = "utf-8"
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(path, "rb")
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(
            fp,
            pagenos,
            maxpages=maxpages,
            password=password,
            caching=caching,
            check_extractable=True,
        ):
            interpreter.process_page(page)

        text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()

    except Exception as exc:
        print(f": there was trouble: {exc}.\n: please enter a valid pdf")
        sys.exit()
    else:
        print(": pdf converted.")
        return text
