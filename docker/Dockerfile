FROM debian:bookworm AS base-image
RUN apt-get update && \
    apt-get install --assume-yes --no-install-recommends python3 && \
    useradd -m --shell /bin/bash -u 1000 non_privileged_user && \
    export SITE_PACKAGE=$(python3 -c "import site;print(site.getsitepackages()[0])")

FROM base-image AS compile-image
RUN apt-get install -y --no-install-recommends make git python3-pip &&\
    pip install --upgrade pip

WORKDIR /usr/app
COPY . .
RUN make install

FROM base-image AS production-image
COPY --from=compile-image $SITE_PACKAGE $SITE_PACKAGE
COPY --from=compile-image /usr/local/bin/auth_service /usr/local/bin/

USER non_privileged_user
CMD auth_service --help
