# See /test/extract/model.py

from cdt.config.references.exercices import NB_AND_PAGE_REFS

def stdvalue(key, value):
    if key in NB_AND_PAGE_REFS:
        nbpages = []

        for nbpage in value.split("|"):
            oneref = []

            for nblike in nbpage.split(","):
                nblike_type, nblike_value = nblike.split(":")

                nblike_type  = nblike_type.strip()
                nblike_value = nblike_value.strip()

                if nblike_type == "empty":
                    oneref.append({'type': nblike_type})

                else:
                    oneref.append({
                        'type' : nblike_type,
                        'value': nblike_value
                    })

            nbpages.append(oneref)

        return nbpages

    elif key == "title":
        return [title.strip() for title in value.split('|')]

    elif key == "date":
        dates = []

        for info in value.split('|'):
            onedate = []

            for nb in info.split('-'):
                nb = nb.strip()

                if nb == "?":
                    nb = None

                else:
                    nb = int(nb)

                onedate.append(nb)

            dates.append(onedate)

        if len(dates) == 1:
            return {
                'kind' : SINGLE_TAG,
                'value': dates[0]
            }

        else:
            return {
                'kind' : RANGE_TAG,
                'start': dates[0],
                'end'  : dates[1]
            }

    elif key == "section":
        level, section = value.split('::')

        return {
            'section': section.strip(),
            'level'  : int(level)
        }

    elif key == "links":
        all_links = []

        for piece in value.split('|'):
            title, url = [
                x.strip()
                for x in piece.split('@')
            ]

            all_links.append({
                "title": title,
                "url"  : url
            })

        return all_links

    elif key == "contexts":
        all_contexts = []

        for piece in value.split('|'):
            thetype, which, value = [
                x.strip()
                for x in piece.split("::")
            ]

            all_contexts.append({
                "type" : thetype.replace('none', ''),
                "which": which.replace('none', ''),
                "value": value
            })

        return all_contexts

    else:
        return [x.strip() for x in value.split("|")]
