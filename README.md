# Family Schemas

This repository currently contains [JSON schemas](https://json-schema.org/) representing the structure
of JSON files used in a family of dataset transformations.

[`pipelines-schema.json`](pipelines-schema.json): details the properties used across a dataset family
and lists the transformation pipelines.

[`dataset-schema.json`](dataset-schema.json): one for each transformation pipeline, providing properties
required for each of the extract, transform and load stages of a pipeline.

[`codelist-schema.json`](codelist-schema.json): actually a [CSV-W table schema](https://www.w3.org/TR/tabular-metadata/#schemas)
capturing the common schema for codelists as CSV.