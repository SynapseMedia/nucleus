sudo sysctl fs.inotify.max_user_watches=582222 && sudo sysctl -p
forever start ~/.nvm/versions/node/v13.12.0/bin/nodemon --exitcrash /data/watchitapi/resource/orbit/local.js $1 $2