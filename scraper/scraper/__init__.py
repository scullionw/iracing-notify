__version__ = "0.1.0"

import logging
import os

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=os.environ.get("LOGLEVEL", logging.INFO),
    datefmt='%Y-%m-%d %H:%M:%S %Z'
)

VIP = {
    "f1": [
        "Max Verstappen",
        "Lando Norris",
        "Jos Verstappen"
        "Carlos Sainz",
        "Charles Leclerc",
        "Antonio Giovinazzi",
        "George Russell",
        "Fernando Alonso",
        "Mick Schumacher",
        "Nicholas Latifi",
    ],
    "ex_f1": [
        "Alexander Albon",
        "Romain Grosjean",
        "Stoffel Vandoorne",
        "Robert Kubica",
        "Juan Pablo Montoya",
        "Rubens Barrichello",
    ],
    "real": ["Daniel Juncadella", "Shane van Gisbergen"],
    "iracing_elite": [
        "Maximilian Benecke",
        "Max Benecke",
        "Joshua K Rogers",
        "Chris Lulham",
        "Suellio Almeida",
    ],
    "qc": ["David Sirois", "Guillaume Lévesque"],
    "friends": [
        "Sandy Scullion",
        "Charles Asselin",
        "Emrick Vincent",
        "Lou-James Scullion",
        "Nicolas Cool",
        "Samuel Asselin2",
        "Kurtis Duddy2",
        "Paul Asselin",
        "Steven Hatcher",
    ],
}