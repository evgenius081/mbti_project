import datasets
from datasets.tasks import TextClassification

class DataSetBuilder(datasets.GeneratorBasedBuilder):
    """Cornell Rotten Tomatoes movie reviews data."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            features=datasets.Features(
                {
                    "text": datasets.Value("string"), 
                 "label": datasets.features.ClassLabel(names=[
                     "INTJ", "INTP", "ENTJ", "ENTP", 
                     "INFJ", "INFP", "ENFJ", "ENFP",
                     "ISTJ", "ISFJ", "ESTJ", "ESFJ",
                     "ISTP", "ISFP", "ESTP", "ESFP"])}
            ),
            supervised_keys=[""],
            homepage="http://www.cs.cornell.edu/people/pabo/movie-review-data/",
            task_templates=[TextClassification(text_column="quote", label_column="type")],
        )

    def _split_generators(self, dl_manager):
        """Downloads Rotten Tomatoes sentences."""
        archive = dl_manager.download(_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"split_key": "train", "files": dl_manager.iter_archive(archive)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"split_key": "validation", "files": dl_manager.iter_archive(archive)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"split_key": "test", "files": dl_manager.iter_archive(archive)},
            ),
        ]

    def _get_examples_from_split(self, split_key, files):
        """Reads Rotten Tomatoes sentences and splits into 80% train,
        10% validation, and 10% test, as is the practice set out in Jinfeng
        Li, ``TEXTBUGGER: Generating Adversarial Text Against Real-world
        Applications.''
        """
        data_dir = "rt-polaritydata/"
        pos_samples, neg_samples = None, None
        for path, f in files:
            if path == data_dir + "rt-polarity.pos":
                pos_samples = [line.decode("latin-1").strip() for line in f]
            elif path == data_dir + "rt-polarity.neg":
                neg_samples = [line.decode("latin-1").strip() for line in f]
            if pos_samples is not None and neg_samples is not None:
                break

        # 80/10/10 split
        i1 = int(len(pos_samples) * 0.8 + 0.5)
        i2 = int(len(pos_samples) * 0.9 + 0.5)
        train_samples = pos_samples[:i1] + neg_samples[:i1]
        train_labels = (["pos"] * i1) + (["neg"] * i1)
        validation_samples = pos_samples[i1:i2] + neg_samples[i1:i2]
        validation_labels = (["pos"] * (i2 - i1)) + (["neg"] * (i2 - i1))
        test_samples = pos_samples[i2:] + neg_samples[i2:]
        test_labels = (["pos"] * (len(pos_samples) - i2)) + (["neg"] * (len(pos_samples) - i2))

        if split_key == "train":
            return (train_samples, train_labels)
        if split_key == "validation":
            return (validation_samples, validation_labels)
        if split_key == "test":
            return (test_samples, test_labels)
        else:
            raise ValueError(f"Invalid split key {split_key}")

    def _generate_examples(self, split_key, files):
        """Yields examples for a given split of MR."""
        split_text, split_labels = self._get_examples_from_split(split_key, files)
        for text, label in zip(split_text, split_labels):
            data_key = split_key + "_" + text
            feature_dict = {"text": text, "label": label}
            yield data_key, feature_dict

