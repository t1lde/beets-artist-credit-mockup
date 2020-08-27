import musicbrainzngs
import json
import six

# Get Musicbrainz release
# Using: Miki Furuakawa - Mirrors https://musicbrainz.org/release/b4fd552b-6470-4449-9afa-55a3d9dc427a

#RELEASE_INCLUDES = ['artists', 'media', 'recordings', 'release-groups',
#                    'labels', 'artist-credits', 'aliases',
#                    'recording-level-rels', 'work-rels',
#                    'work-level-rels', 'artist-rels', 'release-rels']
#
RELEASE_INCLUDES = ['artists', 'artist-credits', 'artist-rels', 'release-rels', 'url-rels', 'aliases']

res = None

try:
    musicbrainzngs.set_useragent("dev mockup", "0.0", "")
except:
    raise Exception("Halt and catch fire")



prettyprint = lambda x: print(json.dumps(x, indent=1))

config = {'import': {'languages': ['en']}}

# Hacky conversion table,
# should probably use a library for this
ISO_639_1_TO_3 = {
    'aa': 'aar',
    'ab': 'abk',
    'ae': 'ave',
    'af': 'afr',
    'ak': 'aka',
    'am': 'amh',
    'an': 'arg',
    'ar': 'ara',
    'as': 'asm',
    'av': 'ava',
    'ay': 'aym',
    'az': 'aze',
    'ba': 'bak',
    'be': 'bel',
    'bg': 'bul',
    'bi': 'bis',
    'bm': 'bam',
    'bn': 'ben',
    'bo': 'bod',
    'br': 'bre',
    'bs': 'bos',
    'ca': 'cat',
    'ce': 'che',
    'ch': 'cha',
    'co': 'cos',
    'cr': 'cre',
    'cs': 'ces',
    'cu': 'chu',
    'cv': 'chv',
    'cy': 'cym',
    'da': 'dan',
    'de': 'deu',
    'dv': 'div',
    'dz': 'dzo',
    'ee': 'ewe',
    'el': 'ell',
    'en': 'eng',
    'eo': 'epo',
    'es': 'spa',
    'et': 'est',
    'eu': 'eus',
    'fa': 'fas',
    'ff': 'ful',
    'fi': 'fin',
    'fj': 'fij',
    'fo': 'fao',
    'fr': 'fra',
    'fy': 'fry',
    'ga': 'gle',
    'gd': 'gla',
    'gl': 'glg',
    'gn': 'grn',
    'gu': 'guj',
    'gv': 'glv',
    'ha': 'hau',
    'he': 'heb',
    'hi': 'hin',
    'ho': 'hmo',
    'hr': 'hrv',
    'ht': 'hat',
    'hu': 'hun',
    'hy': 'hye',
    'hz': 'her',
    'ia': 'ina',
    'id': 'ind',
    'ie': 'ile',
    'ig': 'ibo',
    'ii': 'iii',
    'ik': 'ipk',
    'io': 'ido',
    'is': 'isl',
    'it': 'ita',
    'iu': 'iku',
    'ja': 'jpn',
    'jv': 'jav',
    'ka': 'kat',
    'kg': 'kon',
    'ki': 'kik',
    'kj': 'kua',
    'kk': 'kaz',
    'kl': 'kal',
    'km': 'khm',
    'kn': 'kan',
    'ko': 'kor',
    'kr': 'kau',
    'ks': 'kas',
    'ku': 'kur',
    'kv': 'kom',
    'kw': 'cor',
    'ky': 'kir',
    'la': 'lat',
    'lb': 'ltz',
    'lg': 'lug',
    'li': 'lim',
    'ln': 'lin',
    'lo': 'lao',
    'lt': 'lit',
    'lu': 'lub',
    'lv': 'lav',
    'mg': 'mlg',
    'mh': 'mah',
    'mi': 'mri',
    'mk': 'mkd',
    'ml': 'mal',
    'mn': 'mon',
    'mr': 'mar',
    'ms': 'msa',
    'mt': 'mlt',
    'my': 'mya',
    'na': 'nau',
    'nb': 'nob',
    'nd': 'nde',
    'ne': 'nep',
    'ng': 'ndo',
    'nl': 'nld',
    'nn': 'nno',
    'no': 'nor',
    'nr': 'nbl',
    'nv': 'nav',
    'ny': 'nya',
    'oc': 'oci',
    'oj': 'oji',
    'om': 'orm',
    'or': 'ori',
    'os': 'oss',
    'pa': 'pan',
    'pi': 'pli',
    'pl': 'pol',
    'ps': 'pus',
    'pt': 'por',
    'qu': 'que',
    'rm': 'roh',
    'rn': 'run',
    'ro': 'ron',
    'ru': 'rus',
    'rw': 'kin',
    'sa': 'san',
    'sc': 'srd',
    'sd': 'snd',
    'se': 'sme',
    'sg': 'sag',
    'sh': 'hbs',
    'si': 'sin',
    'sk': 'slk',
    'sl': 'slv',
    'sm': 'smo',
    'sn': 'sna',
    'so': 'som',
    'sq': 'sqi',
    'sr': 'srp',
    'ss': 'ssw',
    'st': 'sot',
    'su': 'sun',
    'sv': 'swe',
    'sw': 'swa',
    'ta': 'tam',
    'te': 'tel',
    'tg': 'tgk',
    'th': 'tha',
    'ti': 'tir',
    'tk': 'tuk',
    'tl': 'tgl',
    'tn': 'tsn',
    'to': 'ton',
    'tr': 'tur',
    'ts': 'tso',
    'tt': 'tat',
    'tw': 'twi',
    'ty': 'tah',
    'ug': 'uig',
    'uk': 'ukr',
    'ur': 'urd',
    'uz': 'uzb',
    've': 'ven',
    'vi': 'vie',
    'vo': 'vol',
    'wa': 'wln',
    'wo': 'wol',
    'xh': 'xho',
    'yi': 'yid',
    'yo': 'yor',
    'za': 'zha',
    'zh': 'zho',
    'zu': 'zul'}


def _artist_credit_fallback_alias(artist_credit, release={}):
    """Given an artist credit block, attempt to find an alias for the artist with the user's preferred locale
    from all the artist-credits for the artist.
    Optionally, we may have data for a release already, so we can try it first.

    Returns an alias for the artist, or the original artist, if not found.
    """

    artist = artist_credit["artist"]
    artist_name = artist['name']
    credit_name = artist_credit.get('name')

    release_lang = release.get('text-representation', {}).get('language')

    # Comparing by ISO639-3, which musicbrainz seems to use for release languages (but not for aliases!)
    release_lang = ISO_639_1_TO_3.get(release_lang, release_lang)
    preferred_langs = [ISO_639_1_TO_3.get(x, x) for x in config['import']['languages']]

    # If the associated release matches the primary config locale, and has an additional credit name, use it.
    if release_lang and (release_lang == preferred_langs[0]) and credit_name:
        return credit_name

    # Use the canonical artist name as fallback
    artist_name = artist['name']

    # Lookup additional data on how the artist is credited on their releases
    # This could perhaps be cached somehow, if repeated api calls are a problem...
    # (Even just a cache of the last artist would make a difference in this case)
    try:
        res = musicbrainzngs.browse_releases(artist=artist['id'], includes='artist-credits')
    except musicbrainzngs.ResponseError:
        return artist_name

    releases = res['release-list']

    # Look through artist releases to find an artist-credits matching the users
    # preferred languages
    name_candidates = {}
    for release in releases:
        release_lang = release.get('text-representation', {}).get('language')
        release_lang = ISO_639_1_TO_3.get(release_lang, release_lang)

        # Skip releases without a language
        if release_lang is None:
            continue

        if release_lang in preferred_langs:
            # Get artist-credit name matching artist-id
            credit_name = None
            for credit in release['artist-credit']:
                # Skip over credits like x, ft., and, etc
                if (isinstance(credit, six.string_types)):
                    continue
                if credit['artist']['id'] == artist['id']:
                    # Differing credit name is under credit['name'] otherwise, will just give the usual artist
                    # details, without this additional tag
                    credit_name = credit.get('name')
                    break;

            if credit_name is None:
                continue;
       
            name_candidates.setdefault(release_lang, []).append(credit_name)

    # Choose from found credit-names based on preferred languages
    for lang in preferred_langs:
        names = name_candidates.get(lang)
        if names:
            # Just return the first name matching a locale
            # alternatively, we could perhaps pick one based on the newest release, for example
            return names[0]

    # Nothing valid found, fallback to what we had already
    return artist_name


mkartist = lambda id, name: {"artist": {"id":id, "name":name + " Not Found"}}
artists = [ mkartist("6b77d8ef-c405-4846-9d5f-2b93e6533101", "Rei Harakami"), \
            mkartist("895653ce-15c4-46a9-bc24-75eb2a91cf57", "Midori"),\
            mkartist("e4bd942f-592b-4cee-bea2-7e62c0fafd09", "Shinsei Kammatechan"),\
            mkartist("a26f7ca4-d14c-408b-9f9c-c8d847286bd0", "Tokyo Shoegazer"),\
            mkartist("bc7478ed-7fe2-40c9-904d-fe037950f414", "Miki Furukawa")]
fallbacks = list(map(_artist_credit_fallback_alias, artists))
print(fallbacks)
