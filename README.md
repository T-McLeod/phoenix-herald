# Phoenix-herald

## Installation
- Working docker installation
- `docker build -t phoenix-herald:latest .`

## Running
```
docker run -d \
  --name phoenix-herald \
  --restart always \
  -e DISCORD_HOSTED_BY=your-name \
  -e DISCORD_TOKEN=your-secret-token-from-discord \
  phoenix-herald:latest
```
