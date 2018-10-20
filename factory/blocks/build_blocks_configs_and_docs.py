#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from collections import defaultdict
from importlib.machinery import SourceFileLoader
import types

from mistool.os_use import PPath
from mistool.string_use import between
from orpyste.data import ReadBlock


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = PPath(__file__).parent

for parent in THIS_DIR.parents:
    if parent.name == "CdT":
        break


DOC_DIR = parent / 'doc'


PY_CONFIG_DIR = parent / 'cdt/config'
PY_TOOLS_DIR  = parent / 'cdt/tools'

STARTING_PYFILE = """
#!/usr/bin/env python3

# The following ugly constants have been build automatically.

# --- BLOCKS --- #
""".strip()


PEUF_DIR = THIS_DIR / 'contexts'

MODE = {
    "verbatim"  : ":default:",
    "keyval:: :": ["keyval", "verbatim", "containers"],
    "container" : "main"
}


# ------------------------------ #
# -- "EXTRACTORS" IMPLEMENTED -- #
# ------------------------------ #

localextract = SourceFileLoader(
    "cdt.tools.extract",
    str(PY_TOOLS_DIR / "extract.py")
).load_module()

EXTRACTORS_IMPLEMENTED = [
    obj
    for obj in dir(localextract)
    if isinstance(localextract.__dict__.get(obj), types.FunctionType)
]


# ----------- #
# -- TOOLS -- #
# ----------- #

def splitit(names):
    return [x.strip() for x in names.split(" ") if x.strip()]

def extractnames(names):
    containers = []
    namesfound = []

    while(names):
        search = between(names, ['/(', ')'])

# No shortcut used
        if search == None:
            namesfound += splitit(names)
            break

# One shortcut used
        else:
            before, inside, names = search

            before = splitit(before)

            namesfound += before[:-1]
            containers.append(before[-1])

            namesfound += splitit(inside)

            names = names.strip()

# Do we use ``--->`` ?
            if names.startswith("-->"):
                alias, *names = [
                    x.strip()
                    for x in names[3:].split(" ")
                    if x.strip()
                ]
                print("alias --->", alias)

                if names:
                    names = " ".join(names)

                else:
                    names = ""

# Single list of values !
    containers = list(set(containers))
    namesfound = list(set(namesfound))

    return containers, namesfound

def typeswanted(keyvaltouse):
    global EXTRACTORS_IMPLEMENTED

    keyvalandtypes = {}

    for line in keyvaltouse:
        key, *val = line.split("=")

        if len(val) > 1:
            raise ValueError(
                "illegal definition of keys and values, "
                +
                "see << {0} >>".format(line.strip())
            )

        elif len(val) == 0:
            val = ":asit:"

        else:
            val = val[0]

        key, val = key.strip(), val.strip()

        if key in keyvalandtypes:
            raise KeyError("key << {0} >> already used".format(key))

        for txt in [key, val]:
            if txt[0] == txt[-1] == ":":
                txt = txt[1:-1]

                if txt != "asit" and txt not in EXTRACTORS_IMPLEMENTED:
                    raise NotImplementedError(
                        "no function << {0} >> ".format(txt)
                        +
                        "in local ``cdt/tools/extract.py``"
                    )

        keyvalandtypes[key] = val

    return keyvalandtypes

def myrepr(val):
# We sort the keys of dictionaries to not polluate the git messages.
    if isinstance(val, dict):
        _repr = "{"

        for key in sorted(val.keys()):
            _repr += "{0}: {1}, ".format(
                myrepr(key),
                myrepr(val[key])
            )

        _repr = _repr[:-2] + "}"

# We sort the keys of dictionaries to not polluate the git messages.
    elif isinstance(val, (list, tuple)):
        _repr = repr(sorted(list(val)))

# Anything else.
    else:
        _repr = repr(val)

    return _repr


# ---------------------------- #
# -- CONFIG. FOR THE BLOCKS -- #
# ---------------------------- #

print('    * Looking for the configurations...')

pytxt_config = [STARTING_PYFILE]

common_nb        = 0
common_defs_txt  = []
keyval_types_txt = []

all_blocks_for_doc = defaultdict(list)

for ppath in PEUF_DIR.walk("file::**.txt"):
    name = ppath.stem

    print('        + Analysing ``{0}.txt``.'.format(name))

    with ReadBlock(
        content = ppath,
        mode    = MODE
    ) as datas:
        infos = datas.mydict("tree std nosep nonb")

    mode = defaultdict(list)

    for kind, subinfos in infos['main'].items():
        if kind == "verbatim":
            containers, names = extractnames(subinfos["names"])

            all_blocks_for_doc[name.lower()] += names

        elif kind in ["keyval", "multikeyval"]:
            kind = "{0}:: {1}".format(kind, subinfos["seps"])

        else:
            raise ValueError("unknown kind << {0} >>".format(kind))

# Extraction of names and maybe some containers !
        containers, names = extractnames(subinfos["names"])

        mode[kind] = names

    if containers:
        mode["container"] = containers

    mode = dict(mode)
    name = name.upper()

    pytxt_config += [
        "",
        "{0} = {1}".format(name, myrepr(mode))
    ]

# Keys to be used and types for values.
    dictforkeys_name = "{0}_KEYS".format(name)

    del infos['main']
    keystouse = {}
    keysfound = []

    if infos:
        if not keyval_types_txt:
            keyval_types_txt += [
                "",
                "# --- ABOUT KEYS AND THEIR VALUES --- #",
            ]

        keyval_types_txt += [
            "",
            dictforkeys_name + " = {}"
        ]

        for blocknames in sorted(infos.keys()):
            all_blocks_for_doc[name.lower()].append(blocknames)

            keyvaltouse = infos[blocknames]
            whatwewant  = typeswanted(keyvaltouse)

            if "-" in blocknames:
                common_nb  += 1
                common_name = "__COMMON_{0}".format(common_nb)

                if not common_defs_txt:
                    common_defs_txt += [
                        "",
                        "# --- COMMON DEFINITIONS FOR KEYS AND THEIR VALUES --- #",
                    ]


                common_defs_txt += [
                    "",
                    "{0} = {1}".format(common_name, myrepr(whatwewant)),
                ]

                for oneblock in blocknames.split("-"):
                    oneblock = oneblock.strip()

                    if oneblock in keysfound:
                        texttofill = '{0}["{1}"].update({2})'

                    else:
                        keysfound.append(oneblock)

                        texttofill = '{0}["{1}"] = {2}'

                    keyval_types_txt += [
                        texttofill.format(
                            dictforkeys_name,
                            oneblock,
                            common_name
                        )
                    ]

            else:
                oneblock = blocknames.strip()

                if oneblock in keysfound:
                    texttofill = '{0}["{1}"].update({2})'

                else:
                    keysfound.append(oneblock)

                    texttofill = '{0}["{1}"] = {2}'

                keyval_types_txt += [
                    texttofill.format(
                        dictforkeys_name,
                        oneblock,
                        myrepr(whatwewant)
                    )
                ]

#TODO: PB SETTINGS
    break

for lines in [
    common_defs_txt,
    keyval_types_txt
]:
    if lines:
        pytxt_config += lines


# ---------------------------- #
# -- UPDATE THE PYTHON FILE -- #
# ---------------------------- #

pyfile_config = PY_CONFIG_DIR / "blocks.py"
pyfile_config.create("file")

print('        + Updating ``{0}``.'.format(pyfile_config.name))

with pyfile_config.open(
    mode     = "w",
    encoding = "utf-8"
) as pyfile:
    pyfile.write("\n".join(pytxt_config))


# --------------------- #
# -- UPDATE THE DOCS -- #
# --------------------- #

print('        + Updating (?) the doc')

STARTING_DOC = """
this::
    date = XXXX-XX-XX


====================================
???
====================================

???

""".lstrip()


for context, names in all_blocks_for_doc.items():
# Looking for the associated file in the doc.
    ppaths_found = []

    for ppath in DOC_DIR.walk("file::**/{0}.txt".format(context)):
        ppaths_found.append(ppath)

    if len(ppaths_found) == 0:
        raise OSError(
            "missing file in the doc for the context ''{0}''".format(context)
        )

    elif len(ppaths_found) > 1:
        message = [
            "several files in the doc for the context ''{0}''".format(context)
        ]

        for p in ppaths_found:
            message.append("    + {0}".format(p))

        raise OSError("\n".join(message))

    toc_file   = ppaths_found[0]
    content_dir = toc_file.parent / toc_file.stem

    with toc_file.open(
        mode     = "r",
        encoding = "utf-8"
    ) as docfile:
        content = docfile.read()

    blocks_documented = []

    for line in content.split('\n'):
        if line.startswith("    ¨content/"):
            filename = line.split(".txt")[0]

            blocks_documented.append(filename.split("/")[-1])

    errors_found = []

    names.sort()

    padding = max(len(n) for n in names) + 10

    for onename in names:
        one_doc_file = content_dir / (onename + ".txt")

        if not one_doc_file.is_file():
            with one_doc_file.open(
                mode     = "w",
                encoding = "utf-8"
            ) as docfile:
                docfile.write(STARTING_DOC)

        if onename not in blocks_documented:
            onename = onename + ".txt"

            errors_found.append(
                "    ¨content/{0}#TODO".format(
                    onename.ljust(padding)
                )
            )

    if errors_found:
        content = content.replace(
            "content::",
            "content::\n{0}".format("\n".join(errors_found))
        )

        with toc_file.open(
            mode     = "w",
            encoding = "utf-8"
        ) as docfile:
            docfile.write(content)