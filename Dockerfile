FROM ubuntu:20.04 AS final
FROM ubuntu:20.04 as build

WORKDIR /

#Fix source problem with sh
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

ARG GITHUB_PASS
ENV GITHUB_PASS $GITHUB_PASS

RUN apt-get update -yq \
    && DEBIAN_FRONTEND=noninteractive apt-get install git -yq
RUN git clone https://${GITHUB_PASS}:@github.com/loopkeybr/dfu_gw_esp.git --branch v1.1.0

FROM final

RUN apt-get update -yq \
    && DEBIAN_FRONTEND=noninteractive apt-get install pip -yq \
    && DEBIAN_FRONTEND=noninteractive apt-get install python3 -yq \
    && DEBIAN_FRONTEND=noninteractive apt-get install unzip -yq \
    && DEBIAN_FRONTEND=noninteractive apt-get install xxd -yq \
    && DEBIAN_FRONTEND=noninteractive apt-get install jq -yq \
    && DEBIAN_FRONTEND=noninteractive apt-get install wget -yq

COPY --from=build /dfu_gw_esp /dfu_gw_esp
COPY . .

RUN pip install -r requirements.txt

CMD [ "./exec.sh" ]
