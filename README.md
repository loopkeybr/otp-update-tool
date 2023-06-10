# otp-update-tool

################################################################

Import envs:
for i in $(cat .env.docker); do export $i; done

Docker build:

Create .env.build, use .env.build.default as start point
docker build -f Dockerfile -t otp_update_tool $(for i in `cat .env.build`; do out+="--build-arg $i " ; done; echo $out;out="") .

Docker run:

Create .env.docker, use .env.docker.default as start point
docker run --env-file .env.docker otp_update_tool

