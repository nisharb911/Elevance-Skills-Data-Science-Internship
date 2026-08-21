import hashlib
import json
from datetime import datetime
from pathlib import Path


METADATA_FILE = Path(
    "data/processed/web_source_metadata.json"
)


class WebSourceManager:

    def __init__(self):

        self.metadata_file = (
            METADATA_FILE
        )

        self.metadata_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.metadata = (
            self._load_metadata()
        )

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

    def calculate_hash(self, content):

        return hashlib.sha256(
            content.encode(
                "utf-8"
            )
        ).hexdigest()

    def check_source(
        self,
        url,
        content_hash
    ):

        previous = (
            self.metadata[
                "sources"
            ].get(url)
        )

        if previous is None:

            return "new"

        if previous["hash"] != content_hash:

            return "modified"

        return "unchanged"

    def update_source(
        self,
        url,
        content_hash,
        chunk_count
    ):

        self.metadata[
            "sources"
        ][url] = {

            "hash": content_hash,

            "last_updated": (
                datetime.now()
                .isoformat()
            ),

            "chunk_count": chunk_count
        }

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