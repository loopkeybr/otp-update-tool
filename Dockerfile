FROM ubuntu

COPY . .

WORKDIR /

RUN apt-get update -yq \
    && DEBIAN_FRONTEND=noninteractive apt-get install pip -yq \
    && DEBIAN_FRONTEND=noninteractive apt-get install python3 -yq \
    && pip install -r requirements.txt \
    && DEBIAN_FRONTEND=noninteractive apt-get install mosquitto -yq \
    && DEBIAN_FRONTEND=noninteractive apt-get install mosquitto-clients -yq \
    && DEBIAN_FRONTEND=noninteractive apt-get install unzip -yq \
    && DEBIAN_FRONTEND=noninteractive apt-get install xxd -yq \
    && DEBIAN_FRONTEND=noninteractive apt-get install jq -yq \
    && DEBIAN_FRONTEND=noninteractive apt-get install wget -yq


# CMD [ "python3", "app.py" ]
CMD [ "./exec.sh"]

# Define custom function directory
# ARG FUNCTION_DIR="/function"

# FROM public.ecr.aws/docker/library/python:buster as build-image

# # Include global arg in this stage of the build
# ARG FUNCTION_DIR

# # Install aws-lambda-cpp build dependencies
# RUN apt-get update && \
#   apt-get install -y \
#   g++ \
#   make \
#   cmake \
#   unzip \
#   libcurl4-openssl-dev


# # Copy function code
# RUN mkdir -p ${FUNCTION_DIR}
# COPY . ${FUNCTION_DIR}


# # Install the function's dependencies
# RUN pip install \
#     --target ${FUNCTION_DIR} \
#         awslambdaric


# FROM public.ecr.aws/docker/library/python:buster

# RUN apt-get update && \
#   apt-get install -y \
#   g++ \
#   make \
#   cmake \
#   unzip \
#   libcurl4-openssl-dev \
#   mosquitto \
#   mosquitto-clients \
#   unzip \
#   xxd \
#   jq \
#   wget


# # Include global arg in this stage of the build
# ARG FUNCTION_DIR
# # Set working directory to function root directory
# WORKDIR ${FUNCTION_DIR}

# # Copy in the built dependencies
# COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# RUN pip install -r ${FUNCTION_DIR}/requirements.txt 

# ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
# CMD [ "update_gw.handler" ]