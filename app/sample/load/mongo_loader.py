from pymongo import UpdateOne

class data_loader:
    def __init__(self, collection):
        self.collection = collection

    def load_many_docs(self, documents):
        if not documents:
            return

        operations = []

        for doc in documents:
            operations.append(
                UpdateOne(
                    {"patient_id": doc["patient_id"]},
                    {
                        "$setOnInsert": {
                            "patient_id": doc["patient_id"],
                            "personal_infos": doc["personal_infos"]
                        },
                        "$addToSet": {
                            "admissions": {
                                "$each": doc["admissions"]
                            }
                        }
                    },
                    upsert=True
                )
            )

        self.collection.bulk_write(operations)
