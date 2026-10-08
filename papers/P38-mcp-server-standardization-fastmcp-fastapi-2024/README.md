# P38: MCP Server Standardization via fastmcp and FastAPI: Transport Unification, SDK Compatibility, and Multi-Protocol Exposure

> **MCP Server Standardization via fastmcp and FastAPI: Transport Unification, SDK Compatibility, and Multi-Protocol Exposure** / in-house / 2024

## Abstract

同一リポジトリ内でmcp 2.x SDK（FastMCP→MCPServerリネーム）とfastmcp 4.xパッケージが混在しimport互換性が破壊される問題を实名調査。fastmcp 4.xのhttp_app()がStarletteアプリを返しFastAPIにmount可能であることを確認し、全MCPサービス（blender-bpy/evaluator/db/sf-paper-comic）をFastMCP+FastAPI統合パターンで再構築。transport={stdio,sse,http,streamable-http}の切替可能なベースサーバーテンプレートを共通化し、個別サービスと統合ゲートウェイの両方で動作するアーキテクチャを確立。

## Keywords

mcp, fastmcp, fastapi, transport, sdk-compatibility, multi-protocol, stdio, sse, streamable-http

---

## 1. Introduction

Model Context Protocol (MCP) はAIツール統合の標準プロトコルとして急速に普及している。しかし、実際の運用において以下の問題が顕在化した：

1. **SDK互換性の破壊**: `mcp` パッケージは1.xでの `FastMCP` クラスを2.xで `MCPServer` にリネームし、import pathが消失した。一方でPyPIには別パッケージとして `fastmcp` 4.xが存在し、同一リポジトリ内で両者が混在する事態が生じた。
2. **Transportの断絶**: 初期実装ではstdio-onlyが基本であり、HTTP経由でのサービス間連携が困難だった。
3. **FastAPI統合の未確立**: Webエコシステムとの連携にはFastAPIが必須だが、FastMCPとFastAPIの統合パターンが公式に広く文書化されていなかった。

本研究は、EvOpsプロジェクト内の4つの異種MCPサービス（SVG/Blender生成、CLIP評価、SQLite蓄積、SF漫画ストーリーボード）を統一的に再構築し、その過程で得られた知見を体系化する。

## 2. Survey: MCP Transport and SDK Evolution

### 2.1 MCP Specification Versions

| Version | Date | Transports | Key Changes |
|---------|------|------------|-------------|
| 2024-11-05 | Nov 2024 | stdio, SSE | Initial stable spec |
| 2025-draft | 2025 | streamable-http | Stateless HTTP with session management |

### 2.2 Python SDK Landscape

| Package | Version | FastMCP Class | Transport Support | FastAPI Integration |
|---------|---------|---------------|-------------------|---------------------|
| `mcp` | 1.x | `mcp.server.fastmcp.FastMCP` | stdio, SSE | None |
| `mcp` | 2.x | `mcp.server.mcpserver.MCPServer` | stdio, SSE | Limited |
| `fastmcp` | 4.x | `fastmcp.FastMCP` | stdio, SSE, HTTP, streamable-http | `http_app()`, `from_fastapi()`, `mount()` |

**Finding**: `mcp` 2.x は後方互換性を破壊し、`fastmcp` 4.x はより豊富なトランスポートとFastAPI統合機能を提供する。

### 2.3 fastmcp 4.x HTTP API

```python
from fastmcp import FastMCP
mcp = FastMCP("name")

# Returns Starlette ASGI app
starlette_app = mcp.http_app(path="/", transport="http")

# Can be mounted in FastAPI
fastapi_app.mount("/mcp", starlette_app)
```

Supported transports:
- `"http"`: Stateless HTTP POST per tool call. Simplest, no persistent connections.
- `"streamable-http"`: MCP 2025 spec compliant. Supports session initialization and streaming.
- `"sse"`: Server-Sent Events. Bidirectional via separate POST/GET channels.

## 3. Key Findings

### Finding 1: Import Path Divergence

同一リポジトリ内で2種類のimportが混在していた：
- `from fastmcp import FastMCP` → fastmcp 4.x ✅
- `from mcp.server.fastmcp import FastMCP` → mcp 1.x (works), 2.x (ModuleNotFoundError) ❌

**教訓**: 依存を `fastmcp>=4.0` に固定し、全importを統一すべき。

### Finding 2: stdio-only の運用限界

stdio transportはホストプロセスからの直接forkに限定される：
```python
# Client側
params = StdioServerParameters(command=sys.executable, args=["server.py"])
```

これは分散環境やコンテナ間通信に対応できない。HTTP transportへの移行が必須。

### Finding 3: FastAPI + MCP の相補的設計

FastAPIとMCPは役割が分離できる：
- **FastAPI**: `/health`, `/ready`, 管理API, CORS, 認証ミドルウェア
- **MCP**: `/mcp/tools/{name}` ツール実行, `/mcp/tools` 一覧

`create_mcp_app()` テンプレートで共通化し、各サービスで再利用。

### Finding 4: Gateway Composition via mount()

`FastMCP.mount(server, namespace)` を使うと、複数のMCPインスタンスを1つの統合エンドポイントに合成できる：

```python
gateway = FastMCP("gateway")
gateway.mount(blender_mcp, namespace="blender")
gateway.mount(eval_mcp, namespace="evaluator")
```

## 4. Architecture

### 4.1 Individual Service Pattern

```
service/
├── server.py         # FastMCP tools + FastAPI app
└── ...
```

各 `server.py` は：
1. `FastMCP` インスタンスを定義
2. `@mcp.tool()` でツールを登録
3. `app = create_mcp_app(mcp)` でFastAPIアプリを生成
4. `__main__` で `--http` フラグで起動モード切替

### 4.2 Unified Gateway Pattern

```
gateway/
└── server.py          # 全サービスをnamespace付きで統合
```

Gatewayは各サービスの `mcp` インスタンスを `mount()` して、1つのエンドポイントで全ツールにアクセス可能にする。

### 4.3 Transport Flexibility

| Mode | Use Case | Command |
|------|----------|---------|
| stdio | Local SDK client (pi, Claude Desktop) | `python server.py` |
| HTTP | Service-to-service REST | `python server.py --http --port 8001` |
| streamable-http | MCP 2025 compliant clients | `transport="streamable-http"` |
| SSE | Legacy streaming support | `transport="sse"` |

## 5. Implementation

### 5.1 Base Server Template (`mcp/base_server.py`)

```python
def create_mcp_app(mcp: FastMCP, transport="http") -> FastAPI:
    app = FastAPI(title=mcp.name)
    @app.get("/health")
    def health(): return {"status": "ok"}
    mcp_starlette = mcp.http_app(path="/", transport=transport)
    app.mount("/mcp", mcp_starlette)
    return app
```

### 5.2 Service Refactoring Example

```python
# mcp/db/server.py
from fastmcp import FastMCP
from mcp.base_server import create_mcp_app, run_mcp_server

mcp = FastMCP("sotsusei-db")

@mcp.tool()
def save_record(table: str, record: dict) -> dict: ...

app = create_mcp_app(mcp)

if __name__ == "__main__":
    if args.http:
        run_mcp_server(mcp, port=args.port, transport="http")
    else:
        mcp.run(transport="stdio")
```

### 5.3 HTTP Test Client

```python
async def call_tool(base_url, name, arguments):
    url = f"{base_url}/mcp/tools/{name}"
    resp = await httpx.AsyncClient().post(url, json=arguments)
    return resp.json()
```

## 6. Discussion

### 6.1 SDK共存のリスク

`mcp` 2.x と `fastmcp` 4.x は名前空間が競合しない（パッケージ名が異なる）が、開発者の認識が混同しやすい。明示的な `requirements.txt` 制約とimport lintingが必要。

### 6.2 Transport選択の指針

- **開発時**: stdio（シンプル、デバッグ容易）
- **本番分散**: HTTP（ステートレス、ロードバランサー対応）
- **長時間タスク**: streamable-http（進捗報告・キャンセル対応）
- **リアルタイム**: SSE（双方向ストリーミング）

### 6.3 Gateway vs Individual Endpoints

Gatewayはサービスディスカバリをシンプルにするが、個別サービスの独立デプロイメントを妨げる場合がある。現時点では両パターンを提供し、運用フェーズで選択するのが妥当。

## 7. Related Work

- **P17 (MCP Spec)**: Protocol foundation; our work extends it with multi-transport exposure.
- **P18 (A2A)**: Agent-to-Agent protocol; complementary to MCP at orchestration layer.
- **P29 (Jev-Driven MLOps)**: MCP services as the tool layer under Jev control plane.
- **P35 (Unified DSL)**: Pipeline DSL that references MCP tools by their HTTP endpoints.

## 8. Conclusion

本研究により、以下が達成された：
1. **SDK互換性問題の顕在化と解決** — fastmcp 4.xへの統一import
2. **Transport統一** — stdio/HTTP/SSE/streamable-http の切替可能な基盤
3. **FastAPI統合パターンの確立** — `create_mcp_app()` テンプレート
4. **統合Gatewayの構築** — `mount()` によるマルチサービス統合
5. **HTTPテストクライアント** — stdio不要のCI/CD対応テスト

今後の課題：authentication middleware, rate limiting, OpenTelemetry instrumentation, streamable-http 本番適用。
