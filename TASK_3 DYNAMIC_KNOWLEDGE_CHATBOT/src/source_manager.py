import hashlib
import json
from pathlib import Path
from datetime import datetime


METADATA_FILE = Path(
    "data/processed/source_metadata.json"
)


class SourceManager:

    def __init__(self):

        self.metadata_file = METADATA_FILE

        self.metadata_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.metadata = self._load_metadata()

    def _load_metadata(self):

        if not self.metadata_file.exists():

            return {
                "sources": {}
            }

        with open(
            self.metadata_file,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def _calculate_hash(self, file_path):

        sha256 = hashlib.sha256()

        with open(file_path, "rb") as file:

            for block in iter(
                lambda: file.read(4096),
                b""
            ):

                sha256.update(block)

        return sha256.hexdigest()

    def check_source(self, file_path):

        file_path = str(Path(file_path))

        current_hash = self._calculate_hash(
            file_path
        )

        previous_data = self.metadata[
            "sources"
        ].get(file_path)

        if previous_data is None:

            return {
                "status": "new",
                "hash": current_hash
            }

        if previous_data["hash"] != current_hash:

            return {
                "status": "modified",
                "hash": current_hash
            }

        return {
            "status": "unchanged",
            "hash": current_hash
        }

    def update_source(
        self,
        file_path,
        file_hash,
        chunk_count
    ):

        file_path = str(Path(file_path))

        self.metadata[
            "sources"
        ][file_path] = {

            "hash": file_hash,

            "last_updated": (
                datetime.now().isoformat()
            ),

            "chunk_count": chunk_count
        }

        self._save_metadata()

    def _save_metadata(self):

        with open(
            self.metadata_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.metadata,
                file,
                indent=4
            )