from __future__ import annotations

import argparse
import asyncio
import os
from pathlib import Path
import socket
from urllib.parse import urlparse

from .config import load_openai_config
from .verilator_judge import make_timestamped_dir
from .top_agent import TopAgent, TopAgentConfig


def _unset_proxy_envs() -> None:
    for key in (
        "http_proxy",
        "https_proxy",
        "all_proxy",
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "ALL_PROXY",
    ):
        os.environ.pop(key, None)


def _network_preflight(base_url: str | None) -> str | None:
    # If a proxy is configured, verify it is reachable first.
    proxy = (
        os.environ.get("HTTPS_PROXY")
        or os.environ.get("https_proxy")
        or os.environ.get("ALL_PROXY")
        or os.environ.get("all_proxy")
        or os.environ.get("HTTP_PROXY")
        or os.environ.get("http_proxy")
    )
    if proxy:
        p = urlparse(proxy)
        if p.hostname and p.port:
            try:
                with socket.create_connection((p.hostname, p.port), timeout=1.5):
                    pass
            except OSError as e:
                return f"Proxy unreachable: {proxy} ({type(e).__name__}: {e})"

    # Without proxy, ensure API host can be resolved.
    api_host = "api.openai.com"
    if base_url:
        u = urlparse(base_url)
        if u.hostname:
            api_host = u.hostname
    if not proxy:
        try:
            socket.getaddrinfo(api_host, 443)
        except OSError as e:
            return f"Cannot resolve API host '{api_host}' ({type(e).__name__}: {e})"
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="eda-agent")
    sub = parser.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("run", help="Run multi-agent RTL loop")
    m.add_argument("--prompt", required=True, help="Natural language spec")
    m.add_argument("--golden-tb", default=None, help="Optional golden testbench path (e.g. VerilogEval *_test.sv)")
    m.add_argument(
        "--golden-ref",
        default=None,
        help="Optional golden reference/blackbox path (e.g. VerilogEval *_ref.sv defining RefModule)",
    )
    m.add_argument("--model", default=None, help="OpenAI model name (default: env OPENAI_MODEL)")
    m.add_argument("--base-url", default=None, help="OpenAI base_url (default: env OPENAI_BASE_URL)")
    m.add_argument("--api-key", default=None, help="OpenAI API key (default: env OPENAI_API_KEY)")
    m.add_argument("--no-proxy", action="store_true", help="Ignore proxy env vars for this run.")
    m.add_argument(
        "--request-timeout",
        type=float,
        default=None,
        help="OpenAI request timeout in seconds (default: env OPENAI_TIMEOUT or internal default).",
    )
    m.add_argument(
        "--extra-body",
        default=None,
        help="OpenAI extra_body JSON string (default: env OPENAI_EXTRA_BODY)",
    )
    m.add_argument("--runs-root", default="runs", help="Directory to store artifacts")
    m.add_argument("--temperature", type=float, default=0.0)
    m.add_argument("--top-p", type=float, default=1.0)
    m.add_argument("--stream", action="store_true", help="Enable streaming model output")
    m.add_argument("--sim-max-retry", type=int, default=4)
    m.add_argument(
        "--debug-max-trials",
        type=int,
        default=30,
        help="Max Debugger (RTLEditor) edit attempts per failing simulation.",
    )
    m.add_argument("--ablation", action="store_true", help="Ablation mode: only RTL generation + syntax check")
    m.add_argument(
        "--max-completion-tokens",
        "--max-tokens",
        dest="max_completion_tokens",
        type=int,
        default=2000,
        help="Max completion tokens (OpenAI: max_completion_tokens)",
    )
    m.add_argument(
        "--run-timeout",
        type=float,
        default=600.0,
        help="Overall timeout in seconds for a single run.",
    )

    args = parser.parse_args(argv)

    if args.cmd == "run":
        if args.no_proxy:
            _unset_proxy_envs()

        cfg = load_openai_config(
            model=args.model,
            api_key=args.api_key,
            base_url=args.base_url,
            request_timeout=args.request_timeout,
            extra_body=args.extra_body,
            temperature=args.temperature,
            top_p=args.top_p,
            max_completion_tokens=args.max_completion_tokens,
            stream=args.stream,
        )
        if not cfg.api_key:
            raise SystemExit(
                "Missing OPENAI_API_KEY (set env or pass --api-key).",
            )

        runs_root = Path(args.runs_root)
        run_dir = make_timestamped_dir(runs_root, "run")
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "prompt.txt").write_text(args.prompt + "\n", encoding="utf-8")
        net_err = _network_preflight(cfg.base_url)
        if net_err:
            (run_dir / "error.txt").write_text(net_err + "\n", encoding="utf-8")
            print("FAIL")
            print(f"run_dir: {run_dir}")
            print("rtl: ")
            print("testbench: ")
            print(f"error: {net_err}")
            return 2

        agent = TopAgent(
            cfg,
            config=TopAgentConfig(
                sim_max_retry=args.sim_max_retry,
                debug_max_trials=args.debug_max_trials,
                is_ablation=args.ablation,
            ),
        )
        try:
            result = asyncio.run(
                asyncio.wait_for(
                    agent.run(
                        spec=args.prompt,
                        output_dir_per_run=run_dir,
                        golden_tb_path=args.golden_tb,
                        golden_rtl_blackbox_path=args.golden_ref,
                    ),
                    timeout=float(args.run_timeout),
                )
            )
        except asyncio.TimeoutError:
            err = f"Run timed out after {float(args.run_timeout):.1f}s."
            (run_dir / "error.txt").write_text(err + "\n", encoding="utf-8")
            print("FAIL")
            print(f"run_dir: {run_dir}")
            print("rtl: ")
            print("testbench: ")
            print(f"error: {err}")
            return 2

        status = "PASS" if result.is_sim_pass and not result.error else "FAIL"
        print(status)
        print(f"run_dir: {result.output_dir_per_run}")
        print(f"rtl: {result.rtl_path}")
        print(f"testbench: {result.tb_path}")
        if result.error:
            print(f"error: {result.error}")
        return 0 if status == "PASS" else 2

    raise AssertionError("unreachable")
