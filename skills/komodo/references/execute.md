# Komodo v2 Execute API

All requests: `POST /execute/<RequestType>` with the params object as the JSON body. Do not wrap params in `{ "type": "...", "params": { ... } }`.

Most return `Update` — an async job object with status/logs.

## Deployments
- `Deploy` `{"deployment":"name-or-id"}` — docker run (create/start container)
- `StartDeployment` `{"deployment":"name-or-id"}` — start stopped container
- `StopDeployment` `{"deployment":"name-or-id"}` — stop container
- `RestartDeployment` `{"deployment":"name-or-id"}` — restart container
- `PauseDeployment` `{"deployment":"name-or-id"}`
- `UnpauseDeployment` `{"deployment":"name-or-id"}`
- `DestroyDeployment` `{"deployment":"name-or-id"}` — stop + remove container
- `PullDeployment` `{"deployment":"name-or-id"}` — pull latest image
- `BatchDeploy` `{"pattern":"regex-or-name"}` — deploy multiple in parallel
- `BatchDestroyDeployment` `{"pattern":"regex-or-name"}`

## Stacks (Docker Compose)
- `DeployStack` `{"stack":"name-or-id"}` — docker compose up
- `StartStack` `{"stack":"name-or-id"}` — docker compose start
- `StopStack` `{"stack":"name-or-id"}` — docker compose stop
- `RestartStack` `{"stack":"name-or-id"}` — docker compose restart
- `PauseStack` `{"stack":"name-or-id"}` — docker compose pause
- `UnpauseStack` `{"stack":"name-or-id"}`
- `DestroyStack` `{"stack":"name-or-id"}` — docker compose down
- `PullStack` `{"stack":"name-or-id"}` — docker compose pull
- `DeployStackIfChanged` `{"stack":"name-or-id"}` — deploy only if contents changed
- `RunStackService` `{"stack":"name-or-id","service":"svc","command":"cmd"}` — compose run
- `BatchDeployStack` `{"pattern":"regex-or-name"}`
- `BatchDestroyStack` `{"pattern":"regex-or-name"}`
- `BatchPullStack` `{"pattern":"regex-or-name"}`

## Builds
- `RunBuild` `{"build":"name-or-id"}` — run a build
- `CancelBuild` `{"build":"name-or-id"}`
- `BatchRunBuild` `{"pattern":"regex-or-name"}`

## Repos
- `CloneRepo` `{"repo":"name-or-id"}`
- `PullRepo` `{"repo":"name-or-id"}`
- `BuildRepo` `{"repo":"name-or-id"}`
- `CancelRepoBuild` `{"repo":"name-or-id"}`
- `BatchCloneRepo` `{"pattern":"regex-or-name"}`
- `BatchPullRepo` `{"pattern":"regex-or-name"}`
- `BatchBuildRepo` `{"pattern":"regex-or-name"}`

## Procedures & Actions
- `RunProcedure` `{"procedure":"name-or-id"}`
- `RunAction` `{"action":"name-or-id"}`
- `BatchRunProcedure` `{"pattern":"regex-or-name"}`
- `BatchRunAction` `{"pattern":"regex-or-name"}`

## Syncs
- `RunSync` `{"sync":"name-or-id"}`

## Server-level Docker
- `StartContainer` `{"server":"name-or-id","container":"name"}`
- `StopContainer` `{"server":"name-or-id","container":"name"}`
- `RestartContainer` `{"server":"name-or-id","container":"name"}`
- `PauseContainer` `{"server":"name-or-id","container":"name"}`
- `UnpauseContainer` `{"server":"name-or-id","container":"name"}`
- `DestroyContainer` `{"server":"name-or-id","container":"name"}`
- `StartAllContainers` `{"server":"name-or-id"}`
- `StopAllContainers` `{"server":"name-or-id"}`
- `RestartAllContainers` `{"server":"name-or-id"}`
- `PauseAllContainers` `{"server":"name-or-id"}`
- `UnpauseAllContainers` `{"server":"name-or-id"}`
- `DeleteImage` `{"server":"name-or-id","image":"name"}`
- `DeleteVolume` `{"server":"name-or-id","volume":"name"}`
- `DeleteNetwork` `{"server":"name-or-id","network":"name"}`
- `PruneImages` `{"server":"name-or-id"}`
- `PruneContainers` `{"server":"name-or-id"}`
- `PruneVolumes` `{"server":"name-or-id"}`
- `PruneNetworks` `{"server":"name-or-id"}`
- `PruneSystem` `{"server":"name-or-id"}` — full docker system prune (incl. volumes)
- `PruneBuildx` `{"server":"name-or-id"}`
- `PruneDockerBuilders` `{"server":"name-or-id"}`

## Alerters
- `TestAlerter` `{"alerter":"name-or-id"}` — test alert delivery

## Admin
- `BackupCoreDatabase` — backup to compressed jsonl (admin only)
- `GlobalAutoUpdate` — trigger global image poll (admin only)
- `SendAlert` `{"level":"Ok","message":"text"}` — send custom alert
- `ClearRepoCache` — admin only
- `Sleep` `{"duration":{"secs":5,"nanos":0}}`
