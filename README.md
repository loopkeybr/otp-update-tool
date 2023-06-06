# lock-update-tool
Tool for updating Loopkey locks

Need to clone dfu_gw_esp repository to work

git clone git@github.com:loopkeybr/dfu_gw_esp.git

################################################################

Import envs:
for i in $(cat .env.docker); do export $i; done

Docker build:

Create .env.build, use .env.build.default as start point
docker build -f Dockerfile -t lock_update_tool $(for i in `cat .env.build`; do out+="--build-arg $i " ; done; echo $out;out="") .

Docker run:

Create .env.docker, use .env.docker.default as start point
docker run --env-file .env.docker lock_update_tool

