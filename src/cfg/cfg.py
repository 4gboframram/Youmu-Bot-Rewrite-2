#    Copyright (C) 2022  4gboframram

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by

#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
The configuration module for Youmu Bot
Note: Do NOT modify any of the configuration in this file. These are just the default settings.
To modify settings actually used by the bot, modify config.json
"""

import logging
import os
from logging import getLogger, StreamHandler
from typing import Optional, ClassVar

from attrs import define
from cattr.preconf.json import make_converter

logger = getLogger(
    __name__
)  # importing get_logger() from .logging would cause circular import
logger.setLevel(logging.DEBUG)
out = StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s:\t%(message)s")
out.setFormatter(formatter)
logger.addHandler(out)


@define
class BotInfo:
    token: str = ""
    name: str = "Youmu Bot"
    gelbooru_credentials: str = ""
    owners: set[str] = {}
    test_guild_ids: list[int] | None = None
    embed_icon_url: str = (
        "https://cdn.discordapp.com/avatars/847655832169480222/16c78890f9383ec318b4560675410120"
        ".webp?size=2048"
    )
    shard: bool = False
    presences: list[str] = [
        "Gardening in Hakugyokurou",
        "Cooking Yuyuko-sama's dinner",
        "Filling up the fridge for Yuyuko-sama",
        "Myon uwu",
        "Eating watermelon with Yuyuko-sama",
        "Myon?",
        "Being best girl",
        "Needing some sleep",
        "Wanting headpats",
    ]

    ping_messages: list[str] = [
        "There's nothing my Roukanken can't cut!",
        "Everyone talks about my sword Roukanken, but not my other sword Hakurouken. *Sad Hakurouken noises* ",
        'Everyone always says "Youmu best girl", but not "How is best girl?" :(',
        'Me or Reimu? That\'s like asking "Would you rather a brown-haired broke girl or a sweet wife?"',
        "Dammit Yuyuko-sama. The fridge is empty again. You need to stop eating so much!",
        "If it taste bad I can always shove this up your ass~",
        "I cut the heavens. I cut reason. I even cut time itself.",
        "The things that cannot be cut by my Roukanken, forged by youkai, are close to none!",
        "Well I don't know how it look but for some reason I want a sperm emoji... "
        'like this I can say "Hey look... it\'s Myon!"',
        "Error 404: Ping message not found.",
        "I am half-human, half-sperm. I mean ghost!",
        "Watermelon",
    ]


@define
class ArtSearch:
    boorutags_base: list[str] = [
        "sort:random",
        # 'solo',
        "-6%2Bgirls",
        "-comic",
        "-greyscale",
        "-huge_filesize",
        "-animated",
        "-audio",
        "-webm",
        "-absurdres",
        "-monochrome",
    ]
    bad_artists: list[str] = [
        "-nori_tamago",
        "-shiraue_yuu",
        "-hammer_(sunset_beach)",
        "-roke_(taikodon)",
        "-guard_bento_atsushi",
        "-kushidama_minaka",
        "-manarou",
        "-shounen_(hogehoge)",
        "-fusu_(a95101221)",
        "-guard_vent_jun",
        "-teoi_(good_chaos)",
        "-wowoguni",
        "-yadokari_genpachirou",
        "-hydrant_(kasozama)",
        "-e.o.",
        "-fusu_(a95101221)",
        "-nishiuri",
        "-freeze-ex",
        "-yuhito_(ablbex)",
        "-koto_inari",
    ]
    badtags_strict: list[str] = [
        "-underwear",
        "-sideboob",
        "-pov_feet",
        "-underboob",
        "-upskirt",
        "-sexually_suggestive",
        "-ass",
        "-bikini",
        "-spread_legs",
        "-bdsm",
        "-lovestruck",
        "-artificial_vagina",
        "-swimsuit",
        "-covering_breasts",
        "-huge_breasts",
        "-blood",
        "-penetration_gesture",
        "-seductive_smile",
        "-no_bra",
        "-off_shoulder",
        "-breast_hold",
        "-cleavage",
        "-nude",
        "-butt_crack",
        "-naked_apron",
        "-convenient_censoring",
        "-bra",
        "-trapped",
        "-restrained",
        "-skirt_lift",
        "-open_shirt",
        "-underwear",
        "-evil_smile",
        "-evil_grin",
        "-choker",
        "-head_under_skirt",
        "-skeleton",
        "-open_fly",
        "-o-ring_bikini",
        "-middle_finger",
        "-white_bloomers",
        "-hot",
        "-tank_top_lift",
        "-short_shorts",
        "-alternate_breast_size",
        "-belly",
        "-wind_lift",
        "-you_gonna_get_raped",
        "-convenient_leg",
        "-convenient_arm",
        "-downblouse",
        "-torn_clothes",
        "-sweater_lift",
        "-open-chest_sweater",
        "-bunnysuit",
        "-gag",
        "-gagged",
        "-ball_gag",
        "-hanging",
        "-erect_nipples",
        "-head_out_of_frame",
        "-covering",
        "-skirt_around_ankles",
        "-furry",
        "-shirt_lift",
        "-vest_lift",
        "-lifted_by_self",
        "-when_you_see_it",
        "-feet",
        "-thighs",
        "-skirt_hold",
        "-open_dress",
        "-open_clothes",
        "-naked_shirt",
        "-shirt_tug",
        "-hip_vent",
        "-no_panties",
        "-surprised",
        "-onsen",
        "-naked_towel",
        "-have_to_pee",
        "-skirt_tug",
        "-pole_dancing",
        "-stripper_pole",
        "-dimples_of_venus",
        "-topless",
        "-trembling",
        "-no_humans",
        "-creepy",
        "-showgirl_skirt",
        "-cookie_(touhou)",
        "-pov",
        "-fusion",
        "-drugs",
        "-weed",
        "-forced_smile",
        "-mouth_pull",
        "-groin",
        "-corruption",
        "-dark_persona",
        "-arms_behind_head",
        "-crop_top",
        "-gluteal_fold",
        "-pregnant",
        "-younger",
        "-white_swimsuit",
        "-tsundere",
        "-crying",
        "-naked_sheet",
        "-undressing",
        "-parody",
        "-under_covers",
        "-genderswap",
        "-real_life_insert",
        "-what",
        "-confession",
        "-race_queen",
        "-naked_cloak",
        "-latex",
        "-bodysuit",
        "-nazi",
        "-swastika",
        "-strap_slip",
        "-chemise",
        "-see-through",
        "-dark",
        "-bad_anatomy",
        "-poorly_drawn",
        "-messy",
        "-you're_doing_it_wrong",
        "-midriff",
        "-large_breasts",
        "-embarrassed",
        "-smelling",
        "-chains",
        "-collar",
        "-arms_up",
        "-blurry_vision",
        "-obese",
        "-miniskirt",
    ]

    very_bad_tags: list[str] = [
        "-loli",
        "-shota",
    ]  # tags that violate discord tos when in nsfw
    character_tags: dict[str, tuple[str, str]] = {
        "reimu": ("hakurei_reimu", "A broke shrine maiden that can turn you into fumo"),
        "marisa": ("kirisame_marisa", "An ordinary magician that does shrooms, ze~"),
        "youmu": (
            "konpaku_youmu",
            "A half human, half sperm, that can cut anything with her two swords. I mean half ghost!",
        ),
        "yuyuko": (
            "saigyouji_yuyuko",
            'A cute spooky ghost that some people call "fat fuck" because she eats a lot',
        ),
        "sakuya": (
            "izayoi_sakuya",
            "The maid of the Scarlet Devil Mansion that most certainly pads her chest",
        ),
        "flandre": (
            "flandre_scarlet",
            "A cute, yet deadly loli with an overplayed theme that can destroy anything",
        ),
        "remilia": (
            "remilia_scarlet",
            "A cute loli that can manipulate fate itself, but still loses in a fight against a broke girl",
        ),
        "patchouli": (
            "patchouli_knowledge",
            "A smart bookworm that writes magic books, but has asthma so she can't recite her own spells",
        ),
        "cirno": ("cirno", "A cool baka that has 9 as her lucky number"),
        "tenshi": ("hinanawi_tenshi", "Peaches"),
        "meiling": (
            "hong_meiling",
            "Chinese girl obsessed with sleeping instead of working her job as guard of the Scarlet Devil Mansion",
        ),
        "rumia": ("rumia", "T-pose and lightspeed dance"),
        "rinnosuke": (
            "morichika_rinnosuke",
            "A half human, half youkai that can tell you the difference between a rubber glove and a condom.",
        ),
        "murasa": ("murasa_minamitsu", "A spirit that can somehow lead a ship"),
        "mamizou": (
            "futatsuiwa_mamizou",
            "A youkai tanuki that turn into you, but actually hot.",
        ),
        "shou": ("toramaru_shou", "A disciple of the god Bishamonten"),
        "nemuno": (
            "sakata_nemuno",
            "A yamanba who lives in secluded areas of Youkai Mountain.",
        ),
        "eternity": ("eternity_larva", "Butterfly?"),
        "narumi": ("yatadera_narumi", "(Touhou 16) (add description)"),
        "daiyousei": ("daiyousei", "Baka's greatest friend"),
        "ringo": ("ringo_(touhou)", "Feed her more dangos"),
        "kosuzu": (
            "motoori_kosuzu",
            "Main character of Forbidden Scrollery, but who tf reads comics",
        ),
        "akyuu": (
            "hieda_no_akyuu",
            "She'll remember everything you tell her, including after death~",
        ),
        "hatate": ("himekaidou_hatate", "Kakashi Spirit News"),
        "mima": ("mima_(touhou)", "Error 404: Character not found"),
        "sariel": ("sariel_(touhou)", "Angel of Death"),
        "yumemi": (
            "okazaki_yumemi",
            'A human that wants to kidnap you and use you for "research"',
        ),
        "shinki": ("shinki", "Demon world, anyone?"),
        "lily": (
            "lily_white",
            'Spring fairy that fills up with "spring" and moans in Touhou LostWord',
        ),
        "shion": ("yorigami_shion", "The goddess of gacha players"),
        "seiran": ("seiran_(touhou)", "placeholder description"),
        "koakuma": ("koakuma", "Funny little devil that works for Patchouli"),
        "raiko": ("horikawa_raiko", "placeholder description"),
        "okina": ("matara_okina", "placeholder description"),
        "mai": ("teireida_mai", "placeholder description"),
        "satono": ("nishida_satono", "placeholder description"),
        "aunn": ("komano_aun", "placeholder description"),
        "komachi": ("onozuka_komachi", "IS THAT THE GRIM REAPER?!"),
        "wakasagihime": ("wakasagihime", "Sushi?"),
        "toyohime": ("watatsuki_no_toyohime", "Peaches!"),
        "yorihime": (
            "watatsuki_no_yorihime",
            "Has the power of god(s) and anime on her side",
        ),
        "renko": ("usami_renko", "placeholder description"),
        "maribel": ("maribel_hearn", "placeholder description"),
        "nue": ("houjuu_nue", "placeholder description"),
        "iku": ("nagae_iku", "placeholder description"),
        "elly": ("elly_(touhou)", "Maybe it's a dream. Maybe nothing else is real."),
        "kasen": ("ibaraki_kasen", "placeholder description"),
        "keine": ("kamishirasawa_keine", "History"),
        "konngara": ("konngara", "placeholder description"),
        "aya": ("shameimaru_aya", "A friendly tengu that is reeaaaaallly fast"),
        "nitori": ("kawashiro_nitori", "placeholder description"),
        "sumireko": ("usami_sumireko", "placeholder description"),
        "okuu": ("reiuji_utsuho", "placeholder description"),
        "koishi": ("komeiji_koishi", "Shrimp fry?"),
        "mokou": (
            "fujiwara_no_mokou",
            "Cute fire girl that can endure more pain than your dad can exert with his belt",
        ),
        "satori": (
            "komeiji_satori",
            "A cute pink-haired girl that always knows what hentai you've been watching",
        ),
        "wan": ("inubashiri_momiji", "placeholder description"),
        "momiji": ("inubashiri_momiji", "Awooooooo"),
        "ran": (
            "yakumo_ran",
            "Shikigami of the Gap Youkai that evolves from Vulpix with a Fire Stone",
        ),
        "kagerou": ("imaizumi_kagerou", "placeholder description"),
        "reisen": ("reisen_udongein_inaba", "bnnuy"),
        "reisen2": ("reisen", "placeholder description"),
        "rei": ("reisen", "placeholder description"),
        "letty": ("letty_whiterock", "placeholder description"),
        "suwako": ("moriya_suwako", "placeholder description"),
        "shizuha": ("aki_shizuha", "placeholder description"),
        "sanae": (
            "kochiya_sanae",
            'Most of the time called "Green Reimu," she\'s a sister in law and a slut.',
        ),
        "clownpiece": ("clownpiece", "placeholder description"),
        "yukari": (
            "yakumo_yukari",
            'A youkai that can manipulate gaps and is often known as "Gap Hag."',
        ),
        "yuuka": ("kazami_yuuka", "Smug sunflower girl :D"),
        "suika": (
            "ibuki_suika",
            "An alcoholic oni that could beat your dad in a drinking contest.",
        ),
        "sekibanki": ("sekibanki", "Can you do this? *Yeets own head at you*"),
        "wriggle": ("wriggle_nightbug", "bug"),
        "hina": ("kagiyama_hina", "placeholder description"),
        "alice": (
            "alice_margatroid",
            "Marisa's number one simp (please don't kill me that's a joke)",
        ),
        "kyouko": ("kasodani_kyouko", "placeholder description"),
        "kisume": ("kisume", "placeholder description"),
        "nazrin": ("nazrin", "placeholder description"),
        "sukuna": ("sukuna_shinmyoumaru", "placeholder description"),
        "kokoro": ("hata_no_kokoro", "-_-"),
        "yoshika": ("miyako_yoshika", "placeholder description"),
        "seiga": ("kaku_seiga", "placeholder description"),
        "kogasa": ("tatara_kogasa", "The girl with homophobia in her eyes"),
        "futo": ("mononobe_no_futo", "placeholder description"),
        "miko": ("toyosatomimi_no_miko", "placeholder description"),
        "tojiko": ("soga_no_tojiko", "placeholder description"),
        "mystia": ("mystia_lorelei", "placeholder description"),
        "genjii": ("genjii_(touhou)", "placeholder description"),
        "byakuren": ("hijiri_byakuren", "placeholder description"),
        "hecatia": ("hecatia_lapislazuli", "placeholder description"),
        "junko": ("junko_(touhou)", "placeholder description"),
        "sagume": ("kishin_sagume", "placeholder description"),
        "doremy": ("doremy_sweet", "placeholder description"),
        "minoriko": ("aki_minoriko", "placeholder description"),
        "yamame": ("kurodani_yamame", "placeholder description"),
        "yuugi": ("hoshiguma_yuugi", "placeholder description"),
        "parsee": ("mizuhashi_parsee", "placeholder description"),
        "tewi": ("inaba_tewi", "placeholder description"),
        "medicine": ("medicine_melancholy", "placeholder description"),
        "eiki": (
            "shiki_eiki",
            "Judges Hell. Honestly I have no idea what to say about her.",
        ),
        "orin": ("kaenbyou_rin", "placeholder description"),
        "kaguya": (
            "houraisan_kaguya",
            "Queen of calculus. Capable of manipulating the instantaneous and eternal",
        ),
        "eirin": ("yagokoro_eirin", "placeholder description"),
        "kanako": ("yasaka_kanako", "placeholder description"),
        "chen": ("chen", "Cheeeeeeeeeen! *nosebleeds*"),
        "star": ("star_sapphire", "placeholder description"),
        "luna": ("luna_child", "placeholder description"),
        "sunny": (
            "sunny_milk",
            '"Get Sunnymilked" -The entire LostWord Discord server',
        ),
        "eika": ("ebisu_eika", "placeholder description"),
        "urumi": ("ushizaki_urumi", "placeholder description"),
        "kutaka": ("niwatari_kutaka", "placeholder description"),
        "lunasa": ("lunasa_prismriver", "The Violinist of the Prismriver sisters"),
        "lyrica": ("lyrica_prismriver", "The keyboardist of the Prismriver sisters"),
        "merlin": ("merlin_prismriver", "Doot"),
        "prismriver": (
            "lunasa_prismriver+lyrica_prismriver+merlin_prismriver",
            "Merlin, Lunasa, and Lyrica :o",
        ),
        "keiki": ("haniyasushin_keiki", "placeholder description"),
        "saki": ("kurokoma_saki", "LEGS!"),
        "mayumi": ("joutouguu_mayumi", "placeholder description"),
        "yachie": ("kicchou_yachie", "placeholder description"),
        "ichirin": ("kumoi_ichirin", "placeholder description"),
        "miyoi": ("okunoda_miyoi", "placeholder description"),
        "chiyuri": ("kitashirakawa_chiyuri", "placeholder description"),
        "pc98": ("touhou_(pc-98)", "placeholder description"),
        "satsuki": ("satsuki_rin", "placeholder description"),
        "tokiko": ("tokiko_(touhou)", "placeholder description"),
        "mimiqwertyuiop": ("mimi-chan", "placeholder description"),
        "kotohime": ("kotohime", "placeholder description"),
        "rikako": ("asakura_rikako", "placeholder description"),
        "ruukoto": ("ruukoto", "placeholder description"),
        "elis": ("elis_(touhou)", "placeholder description"),
        "ellen": ("ellen", "placeholder description"),
        "orange": ("orange_(touhou)", "placeholder description"),
        "benben": ("tsukumo_benben", "placeholder description"),
        "yatsuhashi": ("tsukumo_yatsuhashi", "placeholder description"),
        "mike": ("goutokuji_mike", "placeholder description"),
        "takane": ("yamashiro_takane", "placeholder description"),
        "sannyo": ("komakusa_sannyo", "placeholder description"),
        "chimata": ("tenkyuu_chimata", "placeholder description"),
        "tsukasa": ("kudamaki_tsukasa", "placeholder description"),
        "momoyo": ("himemushi_momoyo", "placeholder description"),
        "misumaru": ("tamatsukuri_misumaru", "placeholder description"),
        "youka": ("kazami_youka", "placeholder description"),
        "kokuu": ("kokuu_haruto", "placeholder description"),
        "hei": ("hei_meiling", "placeholder description"),
        "kongou": ("kongou_(kantai_collection)", "placeholder description"),
        "haruna": ("haruna_(kantai_collection)", "placeholder description"),
        "hiei": ("hiei_(kantai_collection)", "placeholder description"),
        "kirishima": ("kirishima_(kantai_collection)", "placeholder description"),
        "joon": ("yorigami_jo&#039;on", "Like Marisa but a better thief"),
    }


@define
class Reminders:
    db_path: str = "reminders.db"


@define
class Features:
    art_search: ArtSearch = ArtSearch()
    reminders: Reminders = Reminders()


@define
class LoggingInfo:
    logging_level: int = logging.DEBUG
    logging_format: str = "%(asctime)s %(name)s %(levelname)s:\t%(message)s"


@define
class Config:
    """
    A class that represents the configuration info
    """

    bot_info: BotInfo = BotInfo()
    logging_info: LoggingInfo = LoggingInfo()
    features: Features = Features()


class __GetConfig:
    """
    A singleton class that gets configuration either from cache or from the config.json file
    """

    config: ClassVar[Optional[Config]] = None

    def __call__(self, *, force_reload=False) -> Config | None:
        if self.config is not None and not force_reload:
            return self.config

        converter = make_converter()
        if os.path.exists("config.json"):
            logger.debug("Found 'config.json', Loading configuration...")
            with open("config.json") as f:
                type(self).config = converter.loads(f.read(), cl=Config)
            logger.debug("Configuration loaded!")
            # assert self.config is not None
            return self.config
        else:
            logger.error(
                "Could not find config at 'config.json'. Creating a new empty config. "
                "Please fill in your bot information."
            )
            default_config = Config()
            json = converter.dumps(default_config, indent=2)
            with open("config.json", "w+") as f:
                f.write(json)
            exit(1)


get_config = __GetConfig()
