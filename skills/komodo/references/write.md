# Komodo v2 Write API

All requests: `POST /write/<RequestType>` with the params object as the JSON body. Do not wrap params in `{ "type": "...", "params": { ... } }`.

## Servers
- `CreateServer` `{"name":"name","config":{"address":"host:port"}}`
- `UpdateServer` `{"id":"id","config":{...}}`
- `DeleteServer` `{"id":"id"}`
- `RenameServer` `{"id":"id","name":"new-name"}`
- `CopyServer` `{"name":"new-name","id":"source-id"}`

## Deployments
- `CreateDeployment` `{"name":"name","config":{"server_id":"...","image":{"image":"nginx:latest"}}}`
- `CreateDeploymentFromContainer` `{"name":"name","server":"server-id","container":"container-name"}`
- `UpdateDeployment` `{"id":"id","config":{...}}`
- `DeleteDeployment` `{"id":"id"}`
- `RenameDeployment` `{"id":"id","name":"new-name"}`
- `CopyDeployment` `{"name":"new-name","id":"source-id"}`

## Stacks
- `CreateStack` `{"name":"name","config":{"server_id":"...","file_contents":"compose yaml"}}`
- `UpdateStack` `{"id":"id","config":{...}}`
- `WriteStackFileContents` `{"stack":"id","contents":"yaml"}`
- `DeleteStack` `{"id":"id"}`
- `RenameStack` `{"id":"id","name":"new-name"}`
- `CopyStack` `{"name":"new-name","id":"source-id"}`
- `RefreshStackCache` `{"stack":"id"}`

## Builds
- `CreateBuild` `{"name":"name","config":{...}}`
- `UpdateBuild` `{"id":"id","config":{...}}`
- `WriteBuildFileContents` `{"build":"id","contents":"dockerfile"}`
- `DeleteBuild` `{"id":"id"}`
- `RenameBuild` `{"id":"id","name":"new-name"}`
- `CopyBuild` `{"name":"new-name","id":"source-id"}`
- `RefreshBuildCache` `{"build":"id"}`
- `CreateBuildWebhook` `{"build":"id","action":"RunBuild"}`
- `DeleteBuildWebhook` `{"build":"id","action":"RunBuild"}`

## Repos
- `CreateRepo` `{"name":"name","config":{...}}`
- `UpdateRepo` `{"id":"id","config":{...}}`
- `DeleteRepo` `{"id":"id"}`
- `RenameRepo` `{"id":"id","name":"new-name"}`
- `CopyRepo` `{"name":"new-name","id":"source-id"}`
- `RefreshRepoCache` `{"repo":"id"}`
- `CreateRepoWebhook` `{"repo":"id","action":"PullRepo"}`
- `DeleteRepoWebhook` `{"repo":"id","action":"PullRepo"}`

## Procedures
- `CreateProcedure` `{"name":"name","config":{"stages":[...]}}`
- `UpdateProcedure` `{"id":"id","config":{...}}`
- `DeleteProcedure` `{"id":"id"}`
- `RenameProcedure` `{"id":"id","name":"new-name"}`
- `CopyProcedure` `{"name":"new-name","id":"source-id"}`

## Actions
- `CreateAction` `{"name":"name","config":{...}}`
- `UpdateAction` `{"id":"id","config":{...}}`
- `DeleteAction` `{"id":"id"}`
- `RenameAction` `{"id":"id","name":"new-name"}`
- `CopyAction` `{"name":"new-name","id":"source-id"}`
- `CreateActionWebhook` `{"action":"id"}`
- `DeleteActionWebhook` `{"action":"id"}`

## Syncs
- `CreateResourceSync` `{"name":"name","config":{...}}`
- `UpdateResourceSync` `{"id":"id","config":{...}}`
- `CommitSync` `{"sync":"id"}` — export and write to sync file
- `WriteSyncFileContents` `{"sync":"id","contents":"toml"}`
- `RefreshResourceSyncPending` `{"sync":"id"}`
- `DeleteResourceSync` `{"id":"id"}`
- `RenameResourceSync` `{"id":"id","name":"new-name"}`
- `CopyResourceSync` `{"name":"new-name","id":"source-id"}`
- `CreateSyncWebhook` / `DeleteSyncWebhook`

## Alerters
- `CreateAlerter` `{"name":"name","config":{...}}`
- `UpdateAlerter` `{"id":"id","config":{...}}`
- `DeleteAlerter` `{"id":"id"}`
- `RenameAlerter` `{"id":"id","name":"new-name"}`
- `CopyAlerter` `{"name":"new-name","id":"source-id"}`

## Builders
- `CreateBuilder` `{"name":"name","config":{...}}`
- `UpdateBuilder` `{"id":"id","config":{...}}`
- `DeleteBuilder` `{"id":"id"}`
- `RenameBuilder` `{"id":"id","name":"new-name"}`
- `CopyBuilder` `{"name":"new-name","id":"source-id"}`

## Variables (admin only)
- `CreateVariable` `{"name":"name","value":"val","description":"","is_secret":false}`
- `UpdateVariableValue` `{"name":"name","value":"new-val"}`
- `UpdateVariableDescription` `{"name":"name","description":"desc"}`
- `UpdateVariableIsSecret` `{"name":"name","is_secret":true}`
- `DeleteVariable` `{"name":"name"}`

## Tags
- `CreateTag` `{"name":"name"}`
- `RenameTag` `{"id":"id","name":"new-name"}`
- `UpdateTagColor` `{"id":"id","color":"#ff0000"}`
- `DeleteTag` `{"id":"id"}`

## Networking
- `CreateNetwork` `{"server":"id","name":"network-name","driver":"bridge"}`

## Terminals
- `CreateTerminal` `{"server":"id","name":"terminal-name"}`
- `DeleteTerminal` `{"server":"id","name":"terminal-name"}`
- `DeleteAllTerminals` `{"server":"id"}`

## Users & Groups (admin only)
- `CreateLocalUser` `{"username":"name","password":"pw"}`
- `CreateServiceUser` `{"username":"name","description":""}`
- `UpdateUserAdmin` `{"user_id":"id","admin":true}`
- `UpdateUserBasePermissions` `{"user_id":"id","enabled":true}`
- `UpdateServiceUserDescription` `{"user_id":"id","description":""}`
- `DeleteUser` `{"user_id":"id"}`
- `CreateUserGroup` `{"name":"name"}`
- `RenameUserGroup` `{"id":"id","name":"new-name"}`
- `AddUserToUserGroup` `{"user_group":"id","user_id":"id"}`
- `RemoveUserFromUserGroup` `{"user_group":"id","user_id":"id"}`
- `SetUsersInUserGroup` `{"user_group":"id","users":["id1","id2"]}`
- `SetEveryoneUserGroup` `{"user_group":"id","everyone":true}`
- `DeleteUserGroup` `{"id":"id"}`
- `UpdatePermissionOnTarget` `{"user_target":{"type":"User","id":"..."},"resource_target":{"type":"Server","id":"..."},"permission":"Write"}`
- `UpdatePermissionOnResourceType` — set base permission for a type

## Provider Accounts (admin only)
- `CreateDockerRegistryAccount` / `UpdateDockerRegistryAccount` / `DeleteDockerRegistryAccount`
- `CreateGitProviderAccount` / `UpdateGitProviderAccount` / `DeleteGitProviderAccount`
- `CreateApiKeyForServiceUser` `{"user_id":"id","name":"key-name"}`
- `DeleteApiKeyForServiceUser` `{"user_id":"id","key_id":"id"}`

## Resource Meta
- `UpdateResourceMeta` `{"target":{"type":"Server","id":"..."},"meta":{"name":"...","description":"...","tags":[]}}` — update name/description/tags on any resource
