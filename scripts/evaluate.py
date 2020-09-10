import pandas as pd
import openproblems
import openproblems.test.utils


def evaluate_method(task, adata, method):
    output = openproblems.tools.decorators.profile(method)(adata)
    result = {
        "metric": [],
        "value": [],
    }
    for metric in task.METRICS:
        result["metric"].append(metric.__name__)
        result["value"].append(metric(adata))

    del adata
    result = pd.DataFrame(result)
    result["method"] = method.__name__
    result["task"] = task._task_name
    result["memory_mb"] = output["memory_mb"]
    result["memory_leaked_mb"] = output["memory_leaked_mb"]
    result["runtime_s"] = output["runtime_s"]
    return result


def evaluate_dataset(task, dataset):
    adata = dataset(test=False)
    result = []
    for method in task.METHODS:
        r = evaluate_method(task, adata.copy(), method)
        r["dataset"] = dataset.__name__
        result.append(r)

    del adata
    result = pd.concat(result)
    return result


def evaluate_task(task):
    result = []
    for dataset in task.DATASETS:
        result.append(evaluate_dataset(task, dataset))

    result = pd.concat(result)
    return result


def main():
    openproblems.test.utils.ignore_numba_warnings()

    results = []
    for task in openproblems.TASKS:
        task_name = task.__name__.split(".")[-1]
        result = evaluate_task(task).sort_values(["dataset", "metric", "value"])
        with open(
            "../website/content/results/{}.md".format(task_name), "w"
        ) as content_handle, open(
            "../website/results_frontmatter/{}.md".format(task_name), "r"
        ) as frontmatter_handle:
            content_handle.write(frontmatter_handle.read())
            result.to_markdown(content_handle)
        results.append(result)

    results = (
        pd.concat(results)
        .sort_values("value", ascending=False)
        .sort_values(["task", "dataset", "metric"])
    )
    with open("../results.md", "w") as handle:
        results.to_markdown(handle)
    return results


if __name__ == "__main__":
    main()
