import os
import shutil

MLRUNS_DIR = "mlruns"
SERVING_DIR = "src/serving/model"  # final serving folder


def read_metric(path):
    try:
        with open(path) as f:
            line = f.read().strip()
            parts = line.split()
            
            # MLflow format: timestamp value step
            if len(parts) >= 2:
                return float(parts[1])   # ✅ correct value
            else:
                return float(parts[0])
    except:
        return None


def get_all_runs():
    runs = []

    for exp_id in os.listdir(MLRUNS_DIR):
        exp_path = os.path.join(MLRUNS_DIR, exp_id)

        if not os.path.isdir(exp_path):
            continue

        for run_id in os.listdir(exp_path):
            run_path = os.path.join(exp_path, run_id)

            artifacts_path = os.path.join(run_path, "artifacts")
            model_path = os.path.join(artifacts_path, "model")

            # ONLY check model existence
            if not os.path.isdir(model_path):
                continue

            metrics_path = os.path.join(run_path, "metrics")

            recall = read_metric(os.path.join(metrics_path, "recall"))

            print(f"DEBUG: Checking {run_id} → recall={recall}")

            if recall is None:
                continue

            runs.append({
                "exp_id": exp_id,
                "run_id": run_id,
                "path": run_path,
                "recall": recall,
                "f1": read_metric(os.path.join(metrics_path, "f1")) or 0,
                "roc_auc": read_metric(os.path.join(metrics_path, "roc_auc")) or 0
            })

    return runs


def select_best_run(runs):
    runs_sorted = sorted(
        runs,
        key=lambda x: (x["recall"], x["f1"], x["roc_auc"]),
        reverse=True
    )

    return runs_sorted[0]


def copy_best_model(best_run):
    artifacts_path = os.path.join(best_run["path"], "artifacts")

    model_src = os.path.join(artifacts_path, "model")
    feature_src = os.path.join(artifacts_path, "feature_columns.txt")
    preprocess_src = os.path.join(artifacts_path, "preprocessing.pkl")

    # Clean previous serving folder
    if os.path.exists(SERVING_DIR):
        shutil.rmtree(SERVING_DIR)

    os.makedirs(SERVING_DIR, exist_ok=True)

    print(f"\n📦 Copying best model from run: {best_run['run_id']}")

    # Copy model files
    shutil.copytree(model_src, SERVING_DIR, dirs_exist_ok=True)

    # Copy additional artifacts
    shutil.copy(feature_src, os.path.join(SERVING_DIR, "feature_columns.txt"))
    shutil.copy(preprocess_src, os.path.join(SERVING_DIR, "preprocessing.pkl"))

    print(f" Model ready in '{SERVING_DIR}/'")


def main():
    print("🔍 Searching all runs...")

    runs = get_all_runs()

    if not runs:
        print(" No valid runs found")
        return

    print(f"\n Found {len(runs)} valid runs")

    best_run = select_best_run(runs)

    print("\n🏆 Best Run Selected:")
    print(f"   Experiment: {best_run['exp_id']}")
    print(f"   Run ID: {best_run['run_id']}")
    print(f"   Recall: {best_run['recall']}")
    print(f"   F1: {best_run['f1']}")
    print(f"   ROC AUC: {best_run['roc_auc']}")

    copy_best_model(best_run)


if __name__ == "__main__":
    main()