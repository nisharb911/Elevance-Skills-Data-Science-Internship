import time

from apscheduler.schedulers.blocking import BlockingScheduler

from src.updater import KnowledgeBaseUpdater
from src.web_updater import WebKnowledgeUpdater


UPDATE_INTERVAL_MINUTES = 30


def update_knowledge_base():

    print("\n")
    print("=" * 60)
    print("AUTOMATIC KNOWLEDGE BASE UPDATE")
    print("=" * 60)

    print("\nUpdating local documents...")

    document_updater = KnowledgeBaseUpdater()

    document_updater.update_all_sources()

    print("\nUpdating web sources...")

    web_updater = WebKnowledgeUpdater()

    web_updater.update_all_urls()

    print("\n")
    print("=" * 60)
    print("AUTOMATIC UPDATE COMPLETED")
    print("=" * 60)


def main():

    print("=" * 60)
    print("DYNAMIC KNOWLEDGE BASE SCHEDULER")
    print("=" * 60)

    print(
        f"\nUpdate interval: "
        f"Every {UPDATE_INTERVAL_MINUTES} minutes"
    )

    # Run once immediately when scheduler starts.
    update_knowledge_base()

    scheduler = BlockingScheduler()

    scheduler.add_job(
        update_knowledge_base,
        "interval",
        minutes=UPDATE_INTERVAL_MINUTES,
        id="knowledge_base_update",
        replace_existing=True
    )

    print(
        "\nScheduler started successfully."
    )

    print(
        f"The knowledge base will be checked "
        f"every {UPDATE_INTERVAL_MINUTES} minutes."
    )

    print(
        "Press CTRL+C to stop the scheduler."
    )

    try:

        scheduler.start()

    except KeyboardInterrupt:

        print(
            "\nScheduler stopped."
        )


if __name__ == "__main__":

    main()