# Komodo v2 Read API

All requests: `POST /read/<RequestType>` with the params object as the JSON body. Do not wrap params in `{ "type": "...", "params": { ... } }`.

## Servers
- `ListServers` — list servers (params: optional query)
- `ListFullServers` — list with full config
- `GetServer` `{"server":"name-or-id"}` — get specific server
- `GetServerState` `{"server":"name-or-id"}` — server health state
- `GetServerActionState` — current action state
- `GetServersSummary` — counts summary
- `GetSystemStats` `{"server":"name-or-id"}` — CPU/mem/disk stats
- `GetSystemInformation` `{"server":"name-or-id"}` — OS info
- `GetHistoricalServerStats` `{"server":"...","page":0}` — timeseries stats
- `GetPeripheryVersion` `{"server":"name-or-id"}` — agent version

## Deployments
- `ListDeployments` / `ListFullDeployments`
- `GetDeployment` `{"deployment":"name-or-id"}`
- `GetDeploymentActionState` `{"deployment":"name-or-id"}`
- `GetDeploymentContainer` `{"deployment":"name-or-id"}` — container status/image
- `GetDeploymentLog` `{"deployment":"name-or-id","tail":100}` — stdout/stderr logs
- `SearchDeploymentLog` `{"deployment":"name-or-id","query":"error"}` — grep logs
- `GetDeploymentStats` `{"deployment":"name-or-id"}` — docker stats
- `GetDeploymentsSummary`
- `InspectDeploymentContainer` `{"deployment":"name-or-id"}` — full container inspect

## Stacks (Docker Compose)
- `ListStacks` / `ListFullStacks`
- `GetStack` `{"stack":"name-or-id"}`
- `GetStackActionState` `{"stack":"name-or-id"}`
- `GetStackLog` `{"stack":"name-or-id","services":[],"tail":100}`
- `SearchStackLog` `{"stack":"name-or-id","query":"error"}`
- `ListStackServices` `{"stack":"name-or-id"}` — list compose services/containers
- `GetStacksSummary`
- `InspectStackContainer` `{"stack":"name-or-id","service":"service-name"}`

## Builds
- `ListBuilds` / `ListFullBuilds`
- `GetBuild` `{"build":"name-or-id"}`
- `GetBuildActionState` `{"build":"name-or-id"}`
- `GetBuildMonthlyStats` — chart data
- `GetBuildWebhookEnabled` `{"build":"name-or-id"}`
- `ListBuildVersions` `{"build":"name-or-id"}` — past built versions
- `GetBuildsSummary`

## Repos
- `ListRepos` / `ListFullRepos`
- `GetRepo` `{"repo":"name-or-id"}`
- `GetRepoActionState` `{"repo":"name-or-id"}`
- `GetReposSummary`

## Procedures
- `ListProcedures` / `ListFullProcedures`
- `GetProcedure` `{"procedure":"name-or-id"}`
- `GetProcedureActionState` `{"procedure":"name-or-id"}`
- `GetProceduresSummary`

## Actions
- `ListActions` / `ListFullActions`
- `GetAction` `{"action":"name-or-id"}`
- `GetActionActionState` `{"action":"name-or-id"}`
- `GetActionsSummary`

## Syncs
- `ListResourceSyncs` / `ListFullResourceSyncs`
- `GetResourceSync` `{"sync":"name-or-id"}`
- `GetResourceSyncActionState` `{"sync":"name-or-id"}`
- `GetResourceSyncsSummary`

## Alerters & Alerts
- `ListAlerters` / `ListFullAlerters`
- `GetAlerter` `{"alerter":"name-or-id"}`
- `GetAlertersSummary`
- `ListAlerts` `{"page":0}` — paginated alerts list
- `GetAlert` `{"id":"alert-id"}`

## Builders
- `ListBuilders` / `ListFullBuilders`
- `GetBuilder` `{"builder":"name-or-id"}`
- `GetBuildersSummary`

## Docker (Server-level)
- `ListAllDockerContainers` `{"server":"name-or-id"}`
- `ListDockerImages` `{"server":"name-or-id"}`
- `ListDockerVolumes` `{"server":"name-or-id"}`
- `ListDockerNetworks` `{"server":"name-or-id"}`
- `ListComposeProjects` `{"server":"name-or-id"}`
- `InspectDockerContainer` `{"server":"name-or-id","container":"name"}`
- `InspectDockerImage` `{"server":"name-or-id","image":"name"}`
- `InspectDockerVolume` `{"server":"name-or-id","volume":"name"}`
- `InspectDockerNetwork` `{"server":"name-or-id","network":"name"}`
- `GetContainerLog` `{"server":"name-or-id","container":"name","tail":100}`
- `SearchContainerLog` `{"server":"name-or-id","container":"name","query":"error"}`
- `GetDockerContainersSummary` `{"server":"name-or-id"}`
- `ListSystemProcesses` `{"server":"name-or-id"}`

## Variables & Secrets
- `ListVariables`
- `GetVariable` `{"variable":"name"}`
- `ListSecrets`

## Tags
- `ListTags`
- `GetTag` `{"tag":"name-or-id"}`

## Users & Groups
- `ListUsers` (admin only)
- `FindUser` `{"user":"name-or-id"}` (admin only)
- `GetUsername` `{"user_id":"id"}`
- `ListUserGroups`
- `GetUserGroup` `{"user_group":"name-or-id"}`
- `ListPermissions`
- `ListUserTargetPermissions` `{"user_id":"id"}` (admin only)
- `GetPermission` `{"target":{"type":"Server","id":"..."}}`

## Misc
- `GetVersion` — Komodo Core version
- `GetCoreInfo` — core config info
- `ListUpdates` `{"page":0}` — audit log
- `GetUpdate` `{"id":"update-id"}`
- `ListSchedules`
- `ExportAllResourcesToToml`
- `ExportResourcesToToml` `{"resources":{...}}`
