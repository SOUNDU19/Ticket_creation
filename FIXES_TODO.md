# Fixes Required

## 1. Remove "N" letter at top left ✅
- Issue: Logo "NexoraAI" being cut off showing only "N"
- Fix: Check CSS for logo/nav-brand width/overflow

## 2. Remove Department field from Ticket Creation ✅
- File: `frontend/create-ticket.html`
- Remove department dropdown after description

## 3. Remove Department from Profile Page ✅
- File: `frontend/profile.html`
- Remove department field

## 4. Improve ML Model Predictions ✅
- Current model not predicting correctly
- Need to retrain with better algorithm
- Add more diverse training data

## 5. Fix Entity Extraction ✅
- Entities not being extracted from tickets
- Check `backend/ml/predict.py`

## 6. Expand Training Dataset ✅
- Add more realistic support ticket examples
- Cover edge cases
- Improve category distribution

---

## Implementation Plan

### Phase 1: UI Fixes (Quick)
1. Fix logo display
2. Remove department fields

### Phase 2: ML Improvements (Medium)
1. Improve prediction algorithm
2. Add entity extraction
3. Expand dataset

### Phase 3: Testing
1. Test all changes locally
2. Deploy to production
3. Verify predictions

---

## Status: IN PROGRESS
