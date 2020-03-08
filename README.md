# Push Kaggle Kernel

GitHub Action to push Kaggle kernel.

## Example

```yaml
name: Upload Kernel
on:
  push:
    branches:
      - master
jobs:
  upload:
    name: Upload Kernel
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v1
      - uses: harupy/push-kaggle-kernel@master
        env:
          KAGGLE_USERNAME: ${{ secrets.KAGGLE_USERNAME }}
          KAGGLE_KEY: ${{ secrets.KAGGLE_KEY }}
        with:
          slug: ${{ github.sha }}
          title: ${{ github.sha }}
          code_file: ./main.py
          language: python
          kernel_type: script
          is_private: false
          competition_sources: |
            titanic
```
