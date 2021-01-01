# Push Kaggle Kernel

GitHub Action to push Kaggle kernel.

## Usage

1. Add `KAGGLE_USERNAME` and `KAGGLE_KEY` as [secrets][secrets] in your repository.
2. Define your [workflow][workflow].

[secrets]: https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets
[workflow]: https://help.github.com/en/actions/reference/workflow-syntax-for-github-actions

## Example

```yaml
name: Upload

on:
  push:
    branches:
      - master

jobs:
  upload:
    name: Upload
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - uses: harupy/push-kaggle-kernel@master
        env:
          # Do not leak your credentials.
          KAGGLE_USERNAME: ${{ secrets.KAGGLE_USERNAME }}
          KAGGLE_KEY: ${{ secrets.KAGGLE_KEY }}
        with:
          slug: ${{ github.sha }}
          title: ${{ github.sha }}
          code_file: ./script.py
          language: python
          kernel_type: script
          # Do not share high-scoring kernels.
          is_private: false
          competition_sources: |
            titanic
```

## Inputs

| Name                  | Description                                                  | Required | Default   | Options                        |
| :-------------------- | :----------------------------------------------------------- | :------- | :-------- | :----------------------------- |
| `id`                  | ID of kernel (must have the format: {username}/{slug}).      | true     | -         |                                |
| `title`               | Title of kernel (must be at least five characters).          | true     | -         |                                |
| `code_file`           | Path to kernel to push (relative from the repo root).        | true     | -         |                                |
| `language`            | Language that kernel is written in.                          | true     | -         | `["python", "r", "rmarkdown"]` |
| `kernel_type`         | Type of kernel.                                              | true     | -         | `["script", "notebook"]`       |
| `is_private`          | Whether or not kernel should be private.                     | false    | `"true"`  | `["true", "false"]`            |
| `enable_gpu`          | Whether or not kernel should run on a GPU.                   | false    | `"false"` | `["true", "false"]`            |
| `enable_internet`     | Whether or not kernel should be able to access the internet. | false    | `"false"` | `["true", "false"]`            |
| `dataset_sources`     | A list of data sources that kernel should use.               | false    | `""`      |                                |
| `competition_sources` | A list of competition data sources that kernel should use.   | false    | `""`      |                                |
| `kernel_sources`      | A list of kernel data sources that kernel should use.        | false    | `""`      |                                |
