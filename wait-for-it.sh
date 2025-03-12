#!/bin/sh
# wait-for-it.sh

host="$1"
shift
port="$1"
shift
timeout="$1"
shift
cmd="$@"

if [ -z "$host" ] || [ -z "$port" ] || [ -z "$cmd" ]; then
  echo "Usage: $0 host port [timeout] [-- command args]"
  exit 1
fi

if [ -z "$timeout" ]; then
  timeout=15
fi

start=$(date +%s)
end=$((start + timeout))

until nc -z "$host" "$port" 2>/dev/null; do
  now=$(date +%s)
  if [ "$now" -ge "$end" ]; then
    echo "Timed out waiting for $host:$port"
    exit 1
  fi
  sleep 1
done

exec "$@"