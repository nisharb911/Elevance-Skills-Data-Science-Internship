from pathlib import Path
import xml.etree.ElementTree as ET


DATA_DIR = Path("data/raw/MedQuAD")

xml_files = list(DATA_DIR.rglob("*.xml"))

print(f"Total XML files found: {len(xml_files)}")

if not xml_files:
    print("No XML files found.")
    raise SystemExit


sample_file = xml_files[0]

print("\nSample file:")
print(sample_file)


tree = ET.parse(sample_file)
root = tree.getroot()

print("\nRoot:")
print(root.tag)

print("\nRoot attributes:")
print(root.attrib)


# ------------------------------------------------------------
# Document-level information
# ------------------------------------------------------------

focus_element = root.find("Focus")

if focus_element is not None:
    print("\nFocus:")
    print(focus_element.text)


annotations = root.find("FocusAnnotations")

if annotations is not None:

    category = annotations.find("Category")
    umls = annotations.find("UMLS")
    synonyms = annotations.find("Synonyms")

    print("\nFocus Annotations:")

    if category is not None:
        print("Category:", category.text)

    if umls is not None:
        print("UMLS:", umls.text)

    if synonyms is not None:
        print("Synonyms:", synonyms.text)


# ------------------------------------------------------------
# Q&A pairs
# ------------------------------------------------------------

qa_pairs = root.findall(".//QAPair")

print(f"\nQ&A pairs in this file: {len(qa_pairs)}")


for index, qa in enumerate(qa_pairs[:3], start=1):

    print("\n" + "=" * 70)
    print(f"Q&A Pair {index}")
    print("=" * 70)

    print("\nQAPair attributes:")
    print(qa.attrib)

    for child in qa:

        print(f"\n{child.tag}:")

        text = " ".join(child.itertext()).strip()

        print(text[:1000])