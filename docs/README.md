# Documentation

Image preservation, delegate requirements, and generated interfaces.

## Start here

| Need | Owning document |
| --- | --- |
| Use the project | [README.md](../README.md) |
| Change the repository | [AGENTS.md](../AGENTS.md) |
| Deliver or recover | [RELEASING.md](../RELEASING.md) |
| Plan substantial changes | [.specify/memory/project-guide.md](../.specify/memory/project-guide.md) |
| Non-negotiable constraints | [.specify/memory/constitution.md](../.specify/memory/constitution.md) |

## Architecture

[Architecture](architecture.md) owns the shared engine and ImageMagick boundary. The
[catalog](../lib/catalog.json) generates wrappers and reference pages. Domain operations stage
literal filenames and verify output before publication. Metadata, animation, and delegate behavior
must be stated for the actual operation.

## Deployment and recovery

[Requirements](requirements.md) owns supported delegates. [Container usage](docker.md) owns mounts
and invocation. [RELEASING.md](../RELEASING.md) owns source, Pages, and container delivery.
Regenerate catalog-derived surfaces through the existing generator.

## Database and state

There is no application database. Source images remain intact, writes require explicit intent, and
verified output must not overwrite an existing destination. [CLI behavior](cli.md) owns output
rules. [MCP](mcp.md) exposes a restricted read-only surface within configured roots.

## Documentation maintenance

Keep decisions, invariants, failure modes, and recovery requirements in the owning document. Link to
commands, defaults, schemas, and generated catalogs instead of copying them. Change the owner and
affected references together. Update this index when adding or moving a guide, and verify relative
links and heading anchors. Historical specs and audits describe their recorded revision, not current
runtime proof. A topic without an implementation stays explicitly unimplemented.

## Topic guides

- [Contributing](../CONTRIBUTING.md)
- [Architecture](architecture.md)
- [Tool catalog](catalog.md)
- [CLI contract](cli.md)
- [Development environments](development-environments.md)
- [Docker](docker.md)
- [Formats and limits](formats.md)
- [MCP server](mcp.md)
- [Relationship to audio-utils](parity.md)
- [Release procedure](releasing.md)
- [Requirements](requirements.md)
