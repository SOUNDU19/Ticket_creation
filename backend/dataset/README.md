# Dataset Directory

This directory should contain your training datasets for the ML model.

## Dataset Format

The training script automatically detects and loads CSV files from the `datasets/` folder (parent directory).

### Required Columns

Your CSV files should contain at least two columns:
1. **Text/Description column** - The ticket description or issue text
2. **Category/Label column** - The category or classification label

### Supported Column Names

The script automatically detects columns with these patterns:

**Text columns:**
- description
- text
- issue
- ticket
- message
- content

**Category columns:**
- category
- label
- class
- type

### Example Dataset Structure

```csv
description,category
"Application crashes on startup",bug
"Add dark mode feature",feature
"Login page is very slow",performance
"Password reset not working",bug
"Need export to PDF functionality",feature
```

## Dataset Location

The training script looks for datasets in: `../datasets/` (relative to backend directory)

Your datasets are already in the correct location:
```
nexora-ai/
├── datasets/
│   ├── aa_dataset-tickets-multi-lang-5-2-50-version.csv
│   ├── dataset-tickets-german_normalized.csv
│   ├── dataset-tickets-german_normalized_50_5_2.csv
│   ├── dataset-tickets-multi-lang-4-20k.csv
│   └── dataset-tickets-multi-lang3-4k.csv
└── backend/
    └── ml/
        └── train.py
```

## Training the Model

1. Ensure your datasets are in the `datasets/` folder
2. Navigate to the ML directory:
   ```bash
   cd backend/ml
   ```
3. Run the training script:
   ```bash
   python train.py
   ```

The script will:
- Load all CSV files from `datasets/`
- Combine them into a single dataset
- Preprocess the text
- Train multiple ML models
- Select the best performing model
- Save `model.pkl` and `vectorizer.pkl`

## Dataset Requirements

### Minimum Requirements
- At least 100 samples
- At least 2 categories
- Text descriptions should be meaningful (not just keywords)

### Recommended
- 1000+ samples for better accuracy
- 5-10 categories
- Balanced distribution across categories
- Diverse vocabulary and writing styles

## Data Quality Tips

1. **Clean Data:**
   - Remove duplicates
   - Fix typos and formatting
   - Ensure consistent category names

2. **Balanced Categories:**
   - Try to have similar number of samples per category
   - Avoid categories with <10 samples

3. **Meaningful Text:**
   - Descriptions should be complete sentences
   - Include context and details
   - Avoid very short descriptions (<10 words)

4. **Category Naming:**
   - Use lowercase
   - Use underscores for multi-word categories (e.g., "data_loss")
   - Keep names consistent

## Example Categories

Common ticket categories:
- bug
- feature
- performance
- security
- documentation
- enhancement
- question
- support
- technical
- billing

## Troubleshooting

### "No dataset files found"
- Ensure CSV files are in `datasets/` folder
- Check file extensions are `.csv`

### "Could not identify text and category columns"
- Rename columns to match supported patterns
- Or the script will use first two columns as fallback

### Low Accuracy (<95%)
- Add more training data
- Balance category distribution
- Improve data quality
- Add more diverse examples

### Memory Error
- Reduce dataset size
- Process in batches
- Increase system RAM

## Dataset Statistics

After training, the script will display:
- Total samples loaded
- Number of categories
- Category distribution
- Model accuracy metrics

## Adding New Data

To add new training data:
1. Create new CSV file in `datasets/` folder
2. Follow the format above
3. Re-run training script
4. New model will include the additional data

## Data Privacy

⚠️ **Important:**
- Do not include sensitive personal information
- Anonymize user data before training
- Follow data protection regulations (GDPR, etc.)
- Remove PII (names, emails, phone numbers)

---

**Note:** The datasets you provided are already in the correct location and will be automatically loaded during training.
