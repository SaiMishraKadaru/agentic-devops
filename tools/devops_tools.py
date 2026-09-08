import json
import subprocess


def container_status(container_name="postgres"):
    """Return the current status of a Docker container."""
    result = subprocess.run(
        [
            "docker",
            "inspect",
            "--format",
            "{{json .State}}",
            container_name,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    state = json.loads(result.stdout)

    return {
    "container": container_name,
    "status": state["Status"],
    "running": state["Running"],
    "health": state.get("Health", {}).get("Status"),
    "exit_code": state["ExitCode"],
    "error": state["Error"],
    "started_at": state["StartedAt"],
    "finished_at": state["FinishedAt"],
}


def container_logs(container_name="postgres", tail=20):
    """Return recent logs from a Docker container."""
    result = subprocess.run(
        [
            "docker",
            "logs",
            "--tail",
            str(tail),
            container_name,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    return {
        "container": container_name,
        "logs": result.stdout.splitlines(),
    }