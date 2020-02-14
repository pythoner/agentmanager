#!/bin/bash

mongo_url=${MONGO_URL:-"mongodb://isddc-mongodb:27017"}
auth_mode=${API_AUTH_MODE:-"keystone"}

auth_url=${AUTH_URL:-"http://isddc-keystone:5000"}
auth_type=${AUTH_TYPE:-"password"}
project_domain_id=${PROJECT_DOMAIN_ID:-"default"}
user_domain_id=${USER_DOMAIN_ID:-"default"}
project_name=${PROJECT_NAME:-"mini-mon"}
username=${USERNAME:-"mini-mon"}
password=${PASSWORD:-"password"}
api_host=${API_HOST:-"10.121.8.85"}
api_port=${API_PORT:-"30800"}

echo "Updating agentmanager config file with mongo_url"
sed -ie "s~^connection = mongodb://127.0.0.1:27017$~connection = $mongo_url~" /etc/agentmanager/agentmanager.conf
echo "Updating agentmanager config file with username"
sed -ie "s~^admin_user=mini-mon$~admin_user=$username~" /etc/agentmanager/agentmanager.conf
#sed -ie "s~^auth_port=31500$~auth_port=31500~" /etc/agentmanager/agentmanager.conf
echo "Updating agentmanager config file with password"
sed -ie "s~^admin_password=password$~admin_password=$password~" /etc/agentmanager/agentmanager.conf
#sed -ie "s~^auth_protocol=http~auth_protocol=http~" /etc/agentmanager/agentmanager.conf
echo "Updating agentmanager config file with auth_url"
#sed -ie "s~^auth_version=v3$~auth_version=v3~" /etc/agentmanager/agentmanager.conf
sed -ie "s~^identity_uri=http://10.121.12.120:31500$~identity_uri=$auth_url~" /etc/agentmanager/agentmanager.conf
echo "Updating agentmanager config file with project_name"
sed -ie "s~^admin_tenant_name=mini-mon$~admin_tenant_name=$project_name~" /etc/agentmanager/agentmanager.conf
echo "Updating agentmanager config file with auth_host"
#sed -ie "s~^auth_host=10.121.12.120$~auth_host=10.121.12.120~" /etc/agentmanager/agentmanager.conf
echo "Updating agentmanager config file with api_host"
sed -ie "s~^api_host=10.121.8.85~api_host=$api_host~" /etc/agentmanager/agentmanager.conf
echo $api_host 
echo "Updating agentmanager config file with api_port"
echo $api_port_
sed -ie "s~^port=8080~port=$api_port~" /etc/agentmanager/agentmanager.conf

agentmanager-api
