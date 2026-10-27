"""Add a "posibles_significados" list to every abbreviation in the
JSON documents under EtiquetadosIA.

Each abbreviation record already has a "meaning" field with the chosen
interpretation.  The new field will be a list containing *at least* that
interpretation, so that downstream code can treat every entry uniformly as a
list of candidate meanings even when there is only one.  If the field already
exists it will be left untouched (so running the script repeatedly is safe).

Usage::

    python add_posibles_significados.py [root_dir]

If ``root_dir`` is omitted the script searches in
``../Documentacion/EDA/JSON/EtiquetadosIA`` relative to the script file.

The script walks the directory tree recursively and rewrites every
``*.json`` file that contains an ``"abbreviations"`` list.  Files that do not
require modification are left unchanged.
"""

import os
import json
import sys
import csv

# path of the abbreviations file relative to workspace root
CSV_NAME = "abreviaciones.csv"
FIELD_NAME = "candidates"                 # name of the list field stored in JSON
OLD_FIELD = "posibles_significados"       # previous name, for migration


def load_dictionary(csv_path: str) -> dict[str, list[str]]:
    """Read the CSV and return a mapping from abbreviation to list of meanings.

    The file is assumed to have a header with at least two columns:
    Abreviacion,Definicion.  Rows with the same abbreviation accumulate values.
    """
    mapping: dict[str, list[str]] = {}
    try:
        with open(csv_path, encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                abbr = row.get("Abreviacion")
                meaning = row.get("Definicion")
                if abbr and meaning:
                    mapping.setdefault(abbr.strip(), []).append(meaning.strip())
    except FileNotFoundError:
        # caller may ignore if the file isn't present
        pass
    return mapping


def augment_file(path: str, dictionary: dict[str, list[str]]) -> bool:
    """Load a JSON file and add/complete the candidate list field.

    - Migrates ``OLD_FIELD`` to ``FIELD_NAME`` when present.
    - If ``FIELD_NAME`` already exists we extend it with dictionary values.
    - If neither field exists we create ``FIELD_NAME`` containing the chosen
      meaning (if any) and then append dictionary candidates.
    Returns True if the file was modified.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:  # pragma: no cover - helpful for debugging
        print(f"skipping {path}: failed to read ({e})")
        return False

    modified = False

    if isinstance(data, dict) and "abbreviations" in data:
        abbrevs = data.get("abbreviations")
        if isinstance(abbrevs, list):
            for entry in abbrevs:
                if not isinstance(entry, dict):
                    continue

                chosen = entry.get("meaning")
                key = entry.get("text")

                # migrate old field if present
                if OLD_FIELD in entry and FIELD_NAME not in entry:
                    entry[FIELD_NAME] = entry.pop(OLD_FIELD)
                    modified = True

                # start with existing list or chosen meaning
                existing = entry.get(FIELD_NAME)
                if existing is None:
                    if chosen is None:
                        entry[FIELD_NAME] = []
                    else:
                        entry[FIELD_NAME] = [chosen]
                        modified = True
                    existing = entry[FIELD_NAME]

                # now merge dictionary candidates into the new field
                if key and key in dictionary:
                    for candidate in dictionary[key]:
                        if candidate not in existing:
                            existing.append(candidate)
                            modified = True

    if modified:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"updated {path}")
    else:
        print(f"no changes: {path}")
    return modified


def main(root_dir: str) -> None:
    # build dictionary from CSV located next to the script inside prototipoInicial
    csv_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", CSV_NAME))
    dictionary = load_dictionary(csv_path)
    if dictionary:
        print(f"loaded {sum(len(v) for v in dictionary.values())} definitions from {csv_path}")
    else:
        print(f"warning: no dictionary entries found (looked at {csv_path})")

    for dirpath, dirs, files in os.walk(root_dir):
        for fname in files:
            if fname.lower().endswith(".json"):
                augment_file(os.path.join(dirpath, fname), dictionary)


if __name__ == "__main__":
    # the workspace root is three levels above this script (scripts/ -> prototipoInicial/ -> workspace)
    default_root = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "..", "Documentacion", "EDA", "JSON", "EtiquetadosIA")
    )
    root = sys.argv[1] if len(sys.argv) > 1 else default_root
    if not os.path.isdir(root):
        print(f"error: {root} is not a directory")
        sys.exit(1)
    main(root)
