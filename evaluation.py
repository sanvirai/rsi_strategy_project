from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

def evaluate_classification(df):

    # Actual movement (1 = Price goes up, 0 = Price doesn't go up)
    y_true = (df["close"].shift(-1) > df["close"]).astype(int)

    # Strategy prediction (1 = Buy, 0 = No Buy)
    y_pred = df["buy_signal"].astype(int)

    # Remove last row because shift(-1) creates NaN
    y_true = y_true[:-1]
    y_pred = y_pred[:-1]

    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)

    # Evaluation Metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    # Sensitivity = Recall
    sensitivity = recall

    # AUC Score
    try:
        if len(set(y_true)) > 1 and len(set(y_pred)) > 1:
            auc = roc_auc_score(y_true, y_pred)
        else:
            auc = 0.5
    except Exception:
        auc = 0.5

    return {
        "confusion_matrix": cm,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "sensitivity": sensitivity,
        "f1_score": f1,
        "auc": auc
    }