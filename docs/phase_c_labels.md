# Phase C - Barcode-Aligned Labels

The label layer accepts CSV and TSV label tables with a barcode column. Labels are attached by barcode rather than row position, preserving matrix order and leaving unmatched cells unlabeled.

- Duplicate label barcodes raise an error.
- Overlap, unmatched label barcodes, and unlabeled cells are reported.
- Each label column records provenance: `published_10x_reference`, `user_uploaded`, `user_edited`, or another explicit value.

Use `bioml_workbench.data.attach_labels` with an AnnData dataset and a pandas label table.