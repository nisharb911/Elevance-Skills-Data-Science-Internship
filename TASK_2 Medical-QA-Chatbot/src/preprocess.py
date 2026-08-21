from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd
import re
import html
from tqdm import tqdm


# ============================================================
# CONFIGURATION
# ============================================================

RAW_DATA_DIR = Path("data/raw/MedQuAD")
PROCESSED_DATA_DIR = Path("data/processed")

OUTPUT_FILE = PROCESSED_DATA_DIR / "medical_qa.csv"


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):
    """
    Clean and normalize text.

    Important:
    We only normalize whitespace and HTML entities.
    We do not aggressively modify medical content.
    """

    if text is None:
        return ""

    text = html.unescape(text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# EXTRACT ALL TEXT FROM XML ELEMENT
# ============================================================

def get_element_text(element):
    """
    Extract all text from an XML element,
    including nested elements.
    """

    if element is None:
        return ""

    text = " ".join(element.itertext())

    return clean_text(text)


# ============================================================
# FIND XML FILES
# ============================================================

def find_xml_files():

    xml_files = list(
        RAW_DATA_DIR.rglob("*.xml")
    )

    print(
        f"Total XML files found: {len(xml_files)}"
    )

    return xml_files


# ============================================================
# PARSE ONE XML FILE
# ============================================================

def parse_xml_file(xml_file):

    records = []

    try:

        tree = ET.parse(xml_file)

        root = tree.getroot()

    except ET.ParseError as error:

        print(
            f"\nXML parsing error: {xml_file}"
        )

        print(error)

        return records

    # ========================================================
    # DOCUMENT LEVEL INFORMATION
    # ========================================================

    document_id = root.attrib.get(
        "id",
        ""
    )

    source = root.attrib.get(
        "source",
        ""
    )

    url = root.attrib.get(
        "url",
        ""
    )

    # ========================================================
    # FOCUS
    # ========================================================

    focus_element = root.find("Focus")

    focus = get_element_text(
        focus_element
    )

    # ========================================================
    # FOCUS ANNOTATIONS
    # ========================================================

    category = ""

    umls = ""

    synonyms = ""

    annotations = root.find(
        "FocusAnnotations"
    )

    if annotations is not None:

        category_element = annotations.find(
            "Category"
        )

        umls_element = annotations.find(
            "UMLS"
        )

        synonyms_element = annotations.find(
            "Synonyms"
        )

        category = get_element_text(
            category_element
        )

        umls = get_element_text(
            umls_element
        )

        synonyms = get_element_text(
            synonyms_element
        )

    # ========================================================
    # QUESTION ANSWER PAIRS
    # ========================================================

    qa_pairs = root.findall(
        ".//QAPair"
    )

    for index, qa_pair in enumerate(
        qa_pairs,
        start=1
    ):

        # ----------------------------------------------------
        # Question
        # ----------------------------------------------------

        question_element = qa_pair.find(
            "Question"
        )

        question = get_element_text(
            question_element
        )

        # ----------------------------------------------------
        # Answer
        # ----------------------------------------------------

        answer_element = qa_pair.find(
            "Answer"
        )

        answer = get_element_text(
            answer_element
        )

        # ----------------------------------------------------
        # QAPair attributes
        # ----------------------------------------------------

        question_id = qa_pair.attrib.get(
            "id",
            ""
        )

        question_type = qa_pair.attrib.get(
            "qtype",
            ""
        )

        # ----------------------------------------------------
        # If ID isn't available, create one
        # ----------------------------------------------------

        if not question_id:

            question_id = (
                f"{document_id}_{index}"
            )

        # ----------------------------------------------------
        # Store record
        # ----------------------------------------------------

        record = {

            "question_id": question_id,

            "question": question,

            "answer": answer,

            "focus": focus,

            "question_type": question_type,

            "synonyms": synonyms,

            "semantic_type": "",

            "cui": umls,

            "source": source,

            "source_file": str(
                xml_file
            ),

            "url": url
        }

        records.append(record)

    return records


# ============================================================
# REMOVE INVALID RECORDS
# ============================================================

def remove_invalid_records(df):

    before = len(df)

    # Replace missing values
    df["question"] = (
        df["question"]
        .fillna("")
        .astype(str)
    )

    df["answer"] = (
        df["answer"]
        .fillna("")
        .astype(str)
    )

    # Keep records with both question and answer
    df = df[
        (df["question"].str.strip() != "")
        &
        (df["answer"].str.strip() != "")
    ]

    after = len(df)

    print(
        f"Invalid records removed: "
        f"{before - after}"
    )

    return df


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicates(df):

    before = len(df)

    df = df.drop_duplicates(
        subset=[
            "question",
            "answer"
        ]
    )

    after = len(df)

    print(
        f"Duplicate records removed: "
        f"{before - after}"
    )

    return df


# ============================================================
# CLEAN DATAFRAME
# ============================================================

def clean_dataframe(df):

    text_columns = [

        "question",

        "answer",

        "focus",

        "question_type",

        "synonyms",

        "semantic_type",

        "cui",

        "source",

        "source_file",

        "url"
    ]

    for column in text_columns:

        if column in df.columns:

            df[column] = (

                df[column]

                .fillna("")

                .astype(str)

                .apply(clean_text)
            )

    return df


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)

    print(
        "MedQuAD Dataset Preprocessing"
    )

    print("=" * 70)

    # --------------------------------------------------------
    # Check raw dataset
    # --------------------------------------------------------

    if not RAW_DATA_DIR.exists():

        print(
            "\nERROR: MedQuAD dataset "
            "directory not found."
        )

        print(
            f"Expected location: "
            f"{RAW_DATA_DIR}"
        )

        return

    # --------------------------------------------------------
    # Create output directory
    # --------------------------------------------------------

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Find XML files
    # --------------------------------------------------------

    xml_files = find_xml_files()

    if not xml_files:

        print(
            "\nNo XML files found."
        )

        return

    # --------------------------------------------------------
    # Process XML files
    # --------------------------------------------------------

    all_records = []

    print(
        "\nProcessing MedQuAD XML files..."
    )

    for xml_file in tqdm(
        xml_files,
        desc="Processing"
    ):

        records = parse_xml_file(
            xml_file
        )

        all_records.extend(
            records
        )

    # --------------------------------------------------------
    # Extraction result
    # --------------------------------------------------------

    print(
        f"\nTotal extracted QA records: "
        f"{len(all_records)}"
    )

    if not all_records:

        print(
            "\nERROR: No QA records "
            "were extracted."
        )

        return

    # --------------------------------------------------------
    # Create DataFrame
    # --------------------------------------------------------

    df = pd.DataFrame(
        all_records
    )

    print(
        "\nInitial dataset shape:"
    )

    print(df.shape)

    # --------------------------------------------------------
    # Clean
    # --------------------------------------------------------

    df = clean_dataframe(df)

    # --------------------------------------------------------
    # Remove invalid
    # --------------------------------------------------------

    df = remove_invalid_records(
        df
    )

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    df = remove_duplicates(
        df
    )

    # --------------------------------------------------------
    # Reset index
    # --------------------------------------------------------

    df = df.reset_index(
        drop=True
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    df.to_csv(
        OUTPUT_FILE,

        index=False,

        encoding="utf-8-sig"
    )

    # --------------------------------------------------------
    # Final information
    # --------------------------------------------------------

    print("\n" + "=" * 70)

    print(
        "PREPROCESSING COMPLETED"
    )

    print("=" * 70)

    print(
        f"\nFinal number of records: "
        f"{len(df)}"
    )

    print(
        f"\nOutput file:"
    )

    print(
        OUTPUT_FILE
    )

    print(
        "\nFinal dataset shape:"
    )

    print(
        df.shape
    )

    print(
        "\nColumns:"
    )

    for column in df.columns:

        print(
            f"  - {column}"
        )

    # --------------------------------------------------------
    # Sample records
    # --------------------------------------------------------

    print(
        "\nSample records:"
    )

    for index, row in df.head(5).iterrows():

        print(
            "\n" + "-" * 70
        )

        print(
            f"Record {index + 1}"
        )

        print(
            "\nQuestion:"
        )

        print(
            row["question"]
        )

        print(
            "\nAnswer:"
        )

        print(
            row["answer"][:300]
        )

        if len(row["answer"]) > 300:

            print("...")

        print(
            "\nFocus:"
        )

        print(
            row["focus"]
        )

        print(
            "\nQuestion Type:"
        )

        print(
            row["question_type"]
        )

        print(
            "\nSource:"
        )

        print(
            row["source"]
        )


# ============================================================
# EXECUTE
# ============================================================

if __name__ == "__main__":

    main()