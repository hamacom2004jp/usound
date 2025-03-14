
if [[ "${USOUND_DEBUG}" = "true" ]]; then
    DEBUG="--debug"
else
    DEBUG=""
fi
usound -m web -c start --host ${REDIS_HOST} --port ${REDIS_PORT} --password ${REDIS_PASSWORD} --svname ${SVNAME} --listen_port ${LISTEN_PORT} --data /home/${MKUSER}/.usound ${DEBUG}&
if [[ -z "${SVCOUNT}" || "${SVCOUNT}" =~ ^[^0-9]+$ ]]; then
    echo "SVCOUNT is not a number. SVCOUNT=${SVCOUNT}"
    exit 1
fi
for ((i=1; i<${SVCOUNT}; i++))
do
    usound -m server -c start --host ${REDIS_HOST} --port ${REDIS_PORT} --password ${REDIS_PASSWORD} --svname ${SVNAME} --data /home/${MKUSER}/.usound ${DEBUG}&
done
usound -m server -c start --host ${REDIS_HOST} --port ${REDIS_PORT} --password ${REDIS_PASSWORD} --svname ${SVNAME} --data /home/${MKUSER}/.usound ${DEBUG}
