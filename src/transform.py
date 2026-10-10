import pandas as pd
import numpy as np
from .mappings import *
import re


def empty_to_nan(df):
    return df.replace(r"^\s*$", np.nan, regex=True)


def normalize_columns_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
                df.columns.str.lower()
                  .str.replace(":", "")
                  .str.replace(r"\s+", " ", regex=True)
                  .str.strip()
                  .str.replace("ё", "е")
                  .str.replace("\u0301", "") # знак ударения
                  )
    return df


def unite_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    df_start = df.copy()

    result = {}
    for name in df.columns.unique():
        cols = df.loc[:, df.columns == name]
        col = cols.iloc[:, 0]               
        for i in range(1, cols.shape[1]):         
            col = col.fillna(cols.iloc[:, i])      
        result[name] = col

    print(f"Было стобцов: {len(df_start.columns.tolist())}.")
    print(f"Стало столбцов: {len(result.keys())}.")

    return pd.DataFrame(result, index=df.index)


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns=COLUMNS_RENAME_MAP)


def drop_sparse_columns(df: pd.DataFrame, min_fill=0.05) -> pd.DataFrame:
    fill = df.notna().mean()
    for_deletion = fill[fill < min_fill].index
    print(f"Удалено столбцов: {len(for_deletion.tolist())}.") 
    return df.drop(columns=for_deletion)


def drop_service_columns(df: pd.DataFrame) -> pd.DataFrame:
    print(f"Удалено {len(SERVICE_COLUMNS)} столбцов.")
    return df.drop(columns=SERVICE_COLUMNS)


def drop_invalid_price(df: pd.DataFrame) -> pd.DataFrame:
    invalide_price = (df["цена"].str.strip().str.lower().isin(["под заказ", "по запросу"])) | (df["цена"].isna() | (df["цена"].str.contains("%", na=False)))
    print(f"Удалено строк: {invalide_price.sum()}.")
    return df[~invalide_price]


def parse_price(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    text = df["цена"].astype(str).str.replace(r"\s", "", regex=True)
    number = text.str.extract(r"(\d+(?:[.,]\d+)?)", expand=False)
    df["цена"] = pd.to_numeric(number.str.replace(",", "."))
    return df


def drop_zero_price(df: pd.DataFrame) -> pd.DataFrame:
    zero_price = (df["цена"] == 0)
    print(f"Удалено строк: {zero_price.sum()}.")
    return df[~zero_price]


def drop_guitars_with_expensive_items(df: pd.DataFrame) -> pd.DataFrame:
    pattern = "|".join(INCREASE_PRICE_ITEMS)
    has_expensive_items = df["комплектация"].str.lower().str.contains(pattern, na=False)
    print(f"Удалено строк: {has_expensive_items.sum()}.")
    return df[~has_expensive_items]


def drop_guitar_duplicates(df: pd.DataFrame, subset=("название", "цена")) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates(subset=list(subset), keep="first")
    print(f"Удалено дубликатов: {before - len(df)}.")
    return df


def drop_invalid_types(df: pd.DataFrame) -> pd.DataFrame:
    invalid_types = df["тип_инструмента"].str.lower().str.strip().isin(EXCLUDE_TYPES)
    bass = df["название"].str.lower().str.strip().str.contains("бас|bass", na=False)
    to_drop = invalid_types | bass
    print(f"Удалено строк: {to_drop.sum()}")
    return df[~to_drop]



def drop_extra(df: pd.DataFrame) -> pd.DataFrame:
    print(f"Удалено столбцов: {len(EXTRA_COLUMNS)}.")
    return df.drop(columns=EXTRA_COLUMNS)


def rename_brands(df: pd.DataFrame) -> pd.DataFrame:
    print(f"Было уникальных значений: {df['производитель'].nunique()}.")
    new_df = df.copy()
    new_df["производитель"] = df["производитель"].str.lower().str.strip().map(BRAND_RENAME_MAP)
    print(f"Стало уникальных значений: {new_df['производитель'].nunique()}.")
    return new_df


def parse_fret_count(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    print(f"Было уникальных значений: {df['количество_ладов'].nunique()}.")
    count = df["количество_ладов"].astype(str).str.extract(r"^\s*(\d{2})(?!\d)", expand=False)
    new_df["количество_ладов"] = pd.to_numeric(count).astype("float")
    print(f"Стало уникальных значений: {new_df['количество_ладов'].nunique()}.")
    return new_df


def rename_countries(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    print(f"Было уникальных значений: {df['страна_производства'].nunique()}.")
    new_df["страна_производства"] = new_df["страна_производства"].str.lower().\
    str.strip().map(COUNTRY_RENAME_MAP)
    print(f"Стало уникальных значений: {new_df['страна_производства'].nunique()}.")
    return new_df


def rename_neck_joints(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    print(f"Было уникальных значений: {df['крепление_грифа'].nunique()}.")
    new_df["крепление_грифа"] = new_df["крепление_грифа"].str.lower().str.strip().map(NECK_JOINT_RENAME_MAP)
    print(f"Стало уникальных значений: {new_df['крепление_грифа'].nunique()}.")
    return new_df


def parse_weight(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    print(f"Было уникальных значений: {df['вес'].nunique()}.")
    new_df["вес"] = new_df["вес"].str.replace(",", ".").str.extract(r"(\d+(?:\.\d+)?)", expand=False).astype(float)
    print(f"Стало уникальных значений: {new_df['вес'].nunique()}")
    return new_df


def rename_anchor(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    print(f"Было уникальных значений: {df['анкер'].nunique()}.")
    new_df["анкер"] = new_df["анкер"].str.lower().str.strip().map(ANCHOR_RENAME_MAP)
    print(f"Стало уникальных значений: {new_df['анкер'].nunique()}.")
    return new_df


def parse_scale_length(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()

    mm_to_d = lambda x: x / 25.4 if x > 100 else x

    print(f"Было уникальных значений: {df['мензура_общая'].fillna(df['мензура_дюймы']).nunique()}")
    new_df["мензура_общая"] = new_df["мензура_общая"].str.strip().str.replace(",", ".").\
        str.extract(r"^(\d+(?:[.]\d+)?)", expand=False).astype(float).map(mm_to_d).round(1)

    new_df["мензура_дюймы"] = new_df["мензура_дюймы"].str.split(",").str[0].str.strip().str.replace(",", ".").\
        str.extract(r"^(\d+(?:[.]\d+)?)", expand=False).astype(float).round(1)

    new_df["мензура_дюймы"] = new_df["мензура_дюймы"].fillna(new_df["мензура_общая"])
    new_df = new_df.drop(columns=["мензура_общая"])

    print(f"Стало уникальных значений: {new_df['мензура_дюймы'].nunique()}.")

    return new_df


def rename_body_shape(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    print(f"Было уникальных значений: {df['форма_корпуса'].nunique()}")
    new_df["форма_корпуса"] = df["форма_корпуса"].str.lower().str.strip().map(BODY_SHAPE_MAP)
    print(f"Стало уникальных значений: {new_df['форма_корпуса'].nunique()}.")
    return new_df


def drop_guitars_with_wrong_body_shape(df: pd.DataFrame) -> pd.DataFrame:
    has_wrong_shape = df["форма_корпуса"] == "не электрогитара"
    print(f"Удалено строк: {has_wrong_shape.sum()}")
    return df[~has_wrong_shape]


def rename_orientation(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    print(f"Было уникальных значений: {df['ориентация'].nunique()}.")
    new_df["ориентация"] = df["ориентация"].str.lower().str.strip().map(ORIENTATION_RENAME_MAP)
    print(f"Стало уникальных значений: {new_df['ориентация'].nunique()}.")
    return new_df


def rename_string_number(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    print(f"Было уникальных значений: {df['количество_струн'].nunique()}.")
    new_df["количество_струн"] = df["количество_струн"].replace({"61": "6", "6 струн": "6"}).astype(float)
    print(f"Стало уникальных значений: {new_df['количество_струн'].nunique()}.")
    return new_df 


def rename_profile(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    print(f"Было уникальных значений: {df['профиль_грифа'].nunique()}.")
    new_df["профиль_грифа"] = df["профиль_грифа"].str.lower().str.strip().map(PROFILE_RENAME_MAP)
    print(f"Стало уникальных значений: {new_df['профиль_грифа'].nunique()}.")
    return new_df


def rename_finish(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    print(f"Было уникальных значений: {df['отделка_корпуса'].nunique()}.")
    new_df["отделка_корпуса"] = df["отделка_корпуса"].str.lower().str.strip().map(FINISH_RENAME_MAP)
    print(f"Стало уникальных значений: {new_df['отделка_корпуса'].nunique()}.")
    return new_df


def rename_hardware(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    print(f"Было уникальных значений: {df['фурнитура'].nunique()}.")
    new_df["фурнитура"] = df["фурнитура"].str.lower().str.strip().map(HARDWARE_RENAME_MAP)
    print(f"Стало уникальных значений: {new_df['фурнитура'].nunique()}.")
    return new_df


def rename_fretboard(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    print(f"Было уникальных значений: {df['материал_накладки'].nunique()}.")
    new_df["материал_накладки"] = df["материал_накладки"].str.lower().str.strip().replace(FRETBOARD_RENAME_MAP)
    print(f"Стало уникальных значений: {new_df['материал_накладки'].nunique()}.")
    return new_df


def rename_series(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    print(f"Было уникальных значений: {df['серия'].nunique()}.")
    new_df["серия"] = df["серия"].str.lower().str.strip().replace(SERIES_RENAME_MAP)
    print(f"Стало уникальных значений: {new_df['серия'].nunique()}.")
    return new_df


def rename_bridge(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    print(f"Было уникальных значений: {df['бридж'].nunique()}.")
    new_df["бридж"] = df["бридж"].str.lower().str.strip().map(BRIDGE_RENAME_MAP)
    print(f"Стало уникальных значений: {new_df['бридж'].nunique()}.")
    return new_df


def rename_tuners(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    print(f"Было уникальных значений: {df['колки'].nunique()}.")
    new_df["колки"] = df["колки"].str.lower().str.strip().replace(TUNERS_RENAME_MAP)
    print(f"Стало уникальных значений: {new_df['колки'].nunique()}.")
    return new_df


def rename_neck_material(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    print(f"Было уникальных значений: {df['материал_грифа'].nunique()}.")
    new_df["материал_грифа"] = df["материал_грифа"].str.lower().str.strip().replace(NECK_RENAME_MAP)
    print(f"Стало уникальных значений: {new_df['материал_грифа'].nunique()}.")
    return new_df


def rename_pickups(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    new_df["конфигурация_звукоснимателей"] = new_df["конфигурация_звукоснимателей"].fillna(new_df["звукосниматели"])
    new_df = new_df.drop(columns=["звукосниматели"])
    print(f"Было уникальных значений: {new_df['конфигурация_звукоснимателей'].nunique()}.")
    new_df["конфигурация_звукоснимателей"] = new_df["конфигурация_звукоснимателей"].str.lower().str.strip().map(PICKUP_RENAME_MAP)
    print(f"Стало уникальных значений: {new_df['конфигурация_звукоснимателей'].nunique()}.")
    return new_df


def rename_controls(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    print(f"Было уникальных значений: {df['управление'].nunique()}.")
    new_df["управление"] = df["управление"].str.lower().str.strip().map(CONTROLS_RENAME_MAP)
    print(f"Стало уникальных значений: {new_df['управление'].nunique()}.")
    return new_df


def rename_electronics(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    print(f"Было уникальных значений: {df['электроника'].nunique()}.")
    new_df["конфигурация_звукоснимателей"] = new_df["электроника"].where(new_df["электроника"].str.lower().str.strip().isin(["hss", "sss"]),
                                                                         new_df["конфигурация_звукоснимателей"])
    new_df["электроника"] = new_df["электроника"].str.lower().str.strip().map(ELECTRONICS_RENAME_MAP)
    print(f"Стало уникальных значений: {new_df['электроника'].nunique()}.")
    return new_df


def rename_top(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    print(f"Было уникальных значений: {df['материал_топа'].nunique()}.")
    new_df["материал_топа"] = new_df["материал_топа"].str.lower().str.strip().map(TOP_RENAME_MAP)
    print(f"стало уникалбьных значений: {new_df['материал_топа'].nunique()}.")
    return new_df


def extract_brand_series_from_title(df):
    brands = {k.lower(): v for k, v in BRAND_RENAME_MAP.items()}
    pattern = "|".join(re.escape(b) for b in sorted(brands, key=len, reverse=True))
    brand_re = re.compile(rf"(?<!\w)({pattern})(?!\w)", re.I)

    def parse(title):
        text = re.sub(r'\S*[а-яё]\S*', ' ', str(title), flags=re.I)
        m = brand_re.search(text)
        if not m:
            return None, None
        brand = brands[m.group(1).lower()]

        s = re.search(r"([\w'-]+)\s+series\b", text, re.I)
        if s:
            return brand, s.group(1).upper()

        rest = text[m.end():] if text[m.end():].strip() else text[:m.start()]
        words = [w for w in re.findall(r"[\w'.+/-]+", rest) if w.lower() not in ("guitar", "guitars")]
        if not words:
            return brand, None

        first = words[0]
        if re.search(r"\d", first):
            code = first.strip("'").split("-")[0]
            return brand, (re.match(r"[^\W\d_]*", code).group() or code).upper()

        series = [first]
        if first.lower() in ("american", "custom", "classic", "les", "limited", "sun") \
                and len(words) > 1 and not re.search(r"\d", words[1]):
            series.append(words[1])
        if len(words) > len(series) and words[len(series)].upper() in ("II", "III", "IV"):
            series.append(words[len(series)])
        return brand, ' '.join(series).upper()

    new_df = df.copy()
    parsed = [parse(t) for t in new_df["название"]]
    new_df["производитель"] = [b for b, _ in parsed]
    new_df["серия"] = [s for _, s in parsed]
    return new_df


def filter_electric_guitars(df: pd.DataFrame) -> pd.DataFrame:
    def rx(*p):
        return re.compile("|".join(f"(?:{x})" for x in p), re.IGNORECASE)
 
    general = rx(r"общее")
    not_guitar = rx(
        r"^\s*(пикгард|звукоснимател|струны|чехол|кейс|ремень|медиатор)",
        r"балалайк", r"бас-?гитар", r"\bbass\b", r"лэп-?стил", r"\blap\s?steel\b",
    )
    kit = rx(
        r"набор", r"комплект", r"\bbundle\b", r"\bkit\b", r"\bdiy\b",
        r"\bset\b(?!\s*-?\s*neck)(?!-)", r"\b(?:x-|t)?pack\b",
        r"аксессуар", r"медиатор", r"(?<!без )кабел", r"стойк",
        r"\+\s*комбо", r"\bс\s+комбик",
    )
    amp = rx(r"комб(?:ик|оусил)", r"усилител")
    semi_hollow = rx(
        r"полуакуст", r"полупол", r"semi[- ]?(?:acoustic|hollow)",
        r"\bhollow\s*body\b", r"\bhollowbody\b", r"\bhollow\b", r"\bsemi\b",
        r"cent(?:er|re)[- ]?block", r"\barchtop\b", r"арктоп",
        r"\bes-?\d{3}\b", r"uptown kat", r"\bcasino\b", r"\bsheraton\b",
        r"epiphone.*\briviera\b(?!\s+blue)", r"\bartcore\b", r"\bartstar\b",
        r"ibanez.*\b(?:as|af|am|amh|ash|gb|lgb|jsm|fg)\d{2,4}",
        r"gretsch.*\bg?(?:2420|2622|2655|5410|5420|5655|6120|6136)[a-z]*\b",
        r"\bfalcon\b", r"broadkaster", r"gretsch.*nashville",
        r"rickenbacker\s+3\d\d", r"eastman\s+(?:t\d|ar\s?\d)", r"heritage.*\bh-?5\d\d",
        r"verythin", r"hofner.*ignition", r"5th\s+ave", r"godin\s+montreal", r"starfire",
        r"d'?angelico.*\b(?:dc|excel)\b",
        r"(?:sire|larry carlton).*\bh7", r"(?:sire|larry carlton).*\bt7tm\b",
        r"starplayer", r"julietta", r"taylor\s+t3", r"yamaha\s+sa\d",
        r"cort.*\b(?:yorktown|source)\b", r"peerless", r"sigma.*\bhb[aw]-",
    )
    acoustic = rx(
        r"классическ", r"\bclassical\b", r"нейлон", r"\bnylon", r"nylectric",
        r"акустическ", r"acoustasonic", r"\bacoustic\b",
    )
    kids = rx(
        r"детск", r"для дет", r"ребен", r"\bkids?\b", r"уменьшен", r"\b[13]/[24]\b",
        r"\be?mini\b(?![- ]?(?:hum|хамб|switch|toggle))", r"\bmikro\b", r"\bminion\b",
        r"(?<![а-я])мини(?![- ]?(?:хамб|хамбакер|hum|тумблер|переключ))(?![а-я])",
        r"axe heaven", r"миниатюр",                       # сувенирные мини-копии
        r"travel", r"тр[еэ]вел", r"дорожн", r"shorty",
        r"(?<!les paul )(?<!lp )(?<!sg )(?<!dc-)(?<!sc-)\bjunior\b", r"stjunior",
    )
 
    special = rx(
        r"встроен", r"\bс\s+(?:процессор|усилител|комбо)", r"\bgtrs\b", r"nova go", r"silent", r"сайлент", r"\bhush\b",
        r"double\s?-?neck", r"двух?гриф", r"двухголов", r"\beds-?\s?1275\b",
        r"sitar", r"ситар",
    )
 
    artists = (
        "steve vai|paul stanley|rory gallagher|phil collen|satriani|hetfield|marty friedman|"
        "malmsteen|yngwie|stevie ray vaughan|dick dale|stephen carpenter|kirk hammett?|"
        "gus g\\b|danny gatton|jimmy page|holcomb|john 5|clapton|van halen|jeff beck|tremonti|"
        "pete thorn|andre nieri|adrian smith|albert collins|jack white|vandenberg|nita strauss|"
        "jake e\\.? lee|hendroff|andy wood|jake bowen|andy timmons|lifeson|lerxst|malcolm young|"
        "martin miller|myles kennedy|kenny wayne|grehan|angel vivaldi|munky|john osborne|"
        "chrissie hynde|scott lepage|alexi|laiho|skolnick|kotzen|hanneman|broderick|tim henson|"
        "heylmun|schleibaum|jeff loomis|diamond rowe|danhage|sammy duet|brad paisley|george lynch|"
        "misha mansoor|juggernaut|cavestany|mick thomson|chris robertson|mark speer|sgrosso|"
        "dave davidson|jim root|andreas kisser|paul gilbert|satchel|chris buck|brubaker|mustaine|"
        "james valentine|yvette young|sean long|caggiano|shadowcaster|noodles|demmel|rabea|"
        "scott ian|lee malia|john mayer|silver sky|jason richardson|kim thayil|lukather|gary holt|"
        "javier reyes|fluff|petrucci|majesty|nick 13|nergal|ichika|nick johnston|frederiksen|"
        "fredriksen|volsung|kiko|merle haggard|johnny a\\b|grissom|mateus asato|reb beach|"
        "robert cray|robin trower|guthrie govan|ron wood|eklundh|apple horn|nuno|bettencourt|"
        "lari basilio|tom quayle|cazqui|josh smith|nick hipa|stroetzel|mantovanelli|dutkiewicz|"
        "romeo|courtney cox|meshuggah|brandon ellis|caswell|dave murray|demartini|sfogli|dj ashba|"
        "danish pete|kelliher|sparrowhawk|duplantier|agufish|herman li|chelo|zach myers|lettieri|"
        "dustie waring|josh middleton|шомо|shomo|alex wade|kruspe|richard z\\b|rzk|buddy guy|"
        "slash|mike campbell|red dog|landau|mick ronson|"
        "jimi hendrix|hendrix|jimmie vaughan|santana|eric johnson|noel gallagher|johnny marr|"
        "mark thwaite|james burton|christian andreu|cory wong|chris shiflett|nile rodgers|hitmaker|"
        "synyster|kurt cobain|cobain|jag-?stang|troy van leeuwen|jason isbell|mike mccready|"
        "wylde|tom morello|soul power|andy la rocque|john browne|rob scallon|keith merrow|"
        "zacky vengeance|delonge|brian may|jack fowler|jared james nichols|j\\.? ?mascis|"
        "joe strummer|mclaughlin|jake kiszka|kingfish|kenny hickey|"
        "michael amott|tyrant|albert lee|dimebag|\\bdime\\b|razorback|warren haynes|"
        "tony iommi|iommi|greeny|blackie|ryan .?fluff|niederauer|"
        "ibramkhalilov|joe bonamassa|bonamassa|gary moore|peter frampton|adam jones|"
        "jerry cantrell|lzzy hale|billie joe|tak matsumoto|joe walsh|billy gibbons|ace frehley|"
        "tommy thayer|matt heafy|emily wolfe|brent hinds|gary clark|kirk douglas|yungblud|"
        "jason hook|frank iero|duane allman|tracii guns|jersey star|snake sabo|kerry king|"
        "schenker|rusty cooley|steve morse|st\\.? vincent|tosin|abasi|plini|sarah longfield|"
        "brian setzer|setzer|bo diddley|duane eddy|billy duffy|tim armstrong|ritchie blackmore|"
        "billy corgan|tash sultana|steve lacy|ed o'?brien|kurt vile|elvis costello|"
        "mark morton|corey beaulieu|jake pitts|donegan|ultracure|robert smith|machine gun kelly|"
        "jerry horton|jinxx|sullivan king|howorth|patrick stump|zakk|dave grohl|mike kerr|"
        "h\\.e\\.r\\.|andy summers|albert hammond|springsteen|waylon|jim adkins|"
        "brent mason|ken susi|alan ashby|justin beck|cavalera|ted aguilar|ben gibbard|bruno mars|"
        "raphael saadiq|buck owens|charcoal phoenix|voodoo child|tex-?mex|cleaver|triplecaster|mirror telecaster|virginia\"?\\s+strat"
    )
    signature = rx(
        r"signature", r"signatur", r"сигнатур", r"подписн", r"именн", r"\bsig\b",
        r"artist series", r"artist model", r"fender artist",
        artists,
        r"^\W*evh\b|\bevh\b", r"\bwolfgang\b",                     
        r"(?:gibson|epiphone).*randy rhoads", r"jackson usa rr1",
        r"ibanez.*\b(?:jem|pia|uv\d|js\d|ps\d|pgm|frm|atz|kiko|tod\d|thbb|yy\d|ichi|lb1|tqm|"
        r"mmn?\d|m8m|m80m|jbm|jbbm|k7|apex|ndm|slm\d|jiva|egen|tam\d|stm\d|mtm|pwm|ftm|lhm|"
        r"jpm|flatv)",
        r"(?:esp|ltd).*\b(?:kh-?\w*|snakebyte|vulture|iron cross|truckster|kamikaze|gh-?\d|"
        r"gh-sv|gl-?\d*|jh-?\d|as-1|msv|bk-600|jr-?\d|hex|rzk|sd-2|mt-i|jm-i|stef|"
        r"sc-?(?:6\d\d|20\d?|4\d\d|1000|607|608)|gus-|alr|aw-|bb-600|cs-ii|ks m|dv8)\b",
        r"sterling.*\b(?:jp\d+|al\d+p?)\b", r"music man.*\b(?:jp\d+|luke|valentine|kaizen)\b",
        r"washburn.*\bn(?:2|4|24)\b", r"\bnele\b",
        r"gretsch.*g6131-my", r"caparison.*(?:-nh|-jsm|\bmjr\b|-m3 cc|-czq)",
        r"schecter.*\b(?:km-\d|tao-?\d)",
    )
 
    def is_electric(name) -> bool:
        if pd.isna(name):
            return False
        s = re.sub(r"[’‘`´]", "'", str(name).lower().replace("ё", "е")).strip()
        if s in ("", "nan", "none", "null"):
            return False
        if general.search(s) or not_guitar.search(s):
            return False
        if kit.search(s) or (amp.search(s) and "встроен" not in s):
            return False
        if semi_hollow.search(s) or ("thinline" in s and "prs" not in s):
            return False
        if acoustic.search(s) or kids.search(s) or special.search(s) or signature.search(s):
            return False
        return True
 
    return df[df["название"].map(is_electric)].copy()

