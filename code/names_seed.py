"""Seed list of the 91 governors (Parts of the Earth) in diary order, as delivered
by Nalvage, 21-23 May 1584 (Cotton App. XLVI; Casaubon 1659, TFR pp. 140-158).

This list is a working seed only: every name is then checked against
(a) the Casaubon OCR (tfr_check.py), (b) the RPG 2025 Table 1 diary forms for the
16 mismatches, and (c) the letters read from the 1584 table along the sigil paths.
The checked result is data/governors.json.
"""

import json
import sys

AETHYRS = [
    "LIL",
    "ARN",
    "ZOM",
    "PAZ",
    "LAT",
    "MAZ",
    "DEO",
    "ZID",
    "ZIP",
    "ZAX",
    "ICH",
    "LOE",
    "ZIM",
    "VTA",
    "OXO",
    "LEA",
    "TAN",
    "ZEN",
    "POP",
    "CHR",
    "ASP",
    "LIN",
    "TOR",
    "NIA",
    "VTI",
    "DES",
    "ZAA",
    "BAG",
    "RII",
    "TEX",
]

NAMES = """Occodon Pascomb Valgars Doagnis Pacasna Dialiva Samapha Virochi Andispi
Thotanf Axziarg Pothnir Lazdixi Nocamal Tiarpax Saxtomp Vavaamp Zirzird Obmacas
Genadol Aspiaon Zamfres Todnaon Pristac Oddiorg Cralpir Doanzin Lexarph Comanan
Tabitom Molpand Vsnarda Ponodol Tapamal Gedoons Ambriol Gecaond Laparin Docepax
Tedoand Viuipos Ooanamb Tahando Nociabi Tastoxo Cucarpt Lauacon Sochial Sigmorf
Aydropt Tocarzi Nabaomi Zafasai Yalpamb Torzoxi Abaiond Omagrap Zildron Parziba
Totocan Chirspa Toantom Vixpalg Ozidaia Paraoan Calzirg Ronoamb Onizimp Zaxanin
Orcamir Chialps Soageel Mirzind Obvaors Ranglam Pophand Nigrana Bazchim Saziami
Mathula Orpanib Labnixp Focisni Oxlopar Vastrim Odraxti Gomziam Taoagla Gemnimb
Advorpt Dozinal""".split()

assert len(NAMES) == 91, len(NAMES)
out = []
for k, n in enumerate(NAMES):
    a = min(k // 3, 29)
    out.append({"n": k + 1, "aethyr": AETHYRS[a], "aethyr_no": a + 1, "name": n})
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(len(out))
