# gateway-update-tool
Tool for updating Loopkey gateways

Need to clone dfu_gw_esp repository to work

git clone git@github.com:loopkeybr/dfu_gw_esp.git

################################################################
Docker build:

Create .env.build, use .env.build.default as start point
docker build -f Dockerfile -t gateway-update-tool $(for i in `cat .env.build`; do out+="--build-arg $i " ; done; echo $out;out="") .

Docker run:

Create .env.docker, use .env.docker.default as start point
docker run --env-file .env.docker gateway_update_tool

