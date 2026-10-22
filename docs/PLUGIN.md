# Optional Codex plugin

The plugin packages the same [native skill](../skills/m-series-local-helper/SKILL.md).
It adds discovery and installation metadata; it does not add a server, runtime,
background hook, account connection or automatic download. The standalone skill
remains fully usable. Choose one active installation method to avoid duplicate
skill discovery.

## Install from GitHub

On a Mac with a Codex CLI that supports `codex plugin`, ask Codex:

```text
Install the optional Codex plugin from https://github.com/pmcconnon1993-lang/lower-usage-codex-m-series at release v0.1.1. First check whether m-series-local-helper is already installed. Keep one active copy and do not delete my existing skill automatically. Ask my exact chip and RAM before recommending a helper. Model downloads and runtime setup need a separate approved plan.
```

The supported CLI sequence for a new installation is:

```sh
codex plugin marketplace add pmcconnon1993-lang/lower-usage-codex-m-series --ref v0.1.1
codex plugin add lower-usage-codex-m-series@m-series-local-helpers --json
codex plugin list --marketplace m-series-local-helpers --json
```

Then start a new Codex conversation and select **Lower Usage Codex (M Series)**.
Ask for a recommendation and confirm it first asks for missing hardware details.
Successful package installation establishes discovery, not model/runtime readiness.
If your client lacks plugin support, use the standalone skill instructions in the
[README](../README.md); plugin support is optional.

To keep an installed plugin inactive while using an existing standalone skill,
set only this plugin's entry in the supported Codex configuration:

```toml
[plugins."lower-usage-codex-m-series@m-series-local-helpers"]
enabled = false
```

Preserve other settings. Enable it through the plugin UI when choosing the plugin
route, and avoid retaining two active copies of the same instructions. A pinned
marketplace release does not update itself to later releases; review the new
release before changing its ref. The skill's freshness check still reports upstream
changes without installing them.

## Maintainer format

- Root `plugin.json`: Agent Plugins 1.0 portable manifest; `skills/` is discovered
  at its fixed location.
- `.codex-plugin/plugin.json`: compatibility manifest with `skills: "./skills/"`.
  Identity, version, description and presentation must match the root manifest.
- `.agents/plugins/marketplace.json`: Git/repo marketplace. Its `./` source is
  resolved from the repository root, not from the metadata directory.
- A release plugin ZIP includes the two plugin manifests, license, notice and
  skill files. It excludes the marketplace, private records, caches and weights.

This is GitHub distribution, not an approved public OpenAI directory listing or
a cloud-hosted service. Local helper execution requires access to the actual Mac;
a cloud conversation alone cannot reach its loopback service.

Format checked against [OpenAI's plugin packaging documentation](https://developers.openai.com/plugins/build/plugins)
and the installed Codex CLI help on 2026-10-22. Recheck those sources when the
client or manifest standard changes.
