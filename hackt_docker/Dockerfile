FROM ubuntu:16.04 as build

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update && apt-get upgrade -y
RUN apt-get install build-essential automake libtool gawk texinfo -y
RUN apt-get install gcc-4.7 g++-4.7 libreadline5 libncurses5 libncurses5-dev -y

WORKDIR /hackt/build
RUN --mount=type=cache,target=/hackt/build \
    --mount=type=bind,src=deps,target=/hackt/deps \
    tar -C . -xjf /hackt/deps/bison-2.3.tar.bz2 && \
    pushd bison-2.3 && ./configure --prefix=/usr/local && make && make install && popd

RUN --mount=type=cache,target=/hackt/build \
    --mount=type=bind,src=deps,target=/hackt/deps \
    tar -C . -xjf /hackt/deps/flex-2.5.4-2-src.tar.bz2 && \
    pushd flex-2.5.4-2 && ./configure --prefix=/usr/local && make && make install && popd

COPY hackt /hackt/src
WORKDIR /hackt/src
RUN --mount=type=cache,target=/hackt/build \
    --mount=type=bind,src=deps,target=/hackt/deps \
    ./bootstrap && \
    sed -i.orig -e '/link_all_deplibs/s|=no|=yes|' ./config/libtool.m4 && \
    CC=/usr/bin/gcc-4.7 CXX=/usr/bin/g++-4.7 CFLAGS="-O2 -Wno-error" CXXFLAGS="-O2 -Wno-error" ./configure --disable-strict-dialect --disable-docs --prefix=/usr/local && \
    make && make test && make install

FROM ubuntu:16.04

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get upgrade -y \
    && apt install -y libtool texinfo libreadline5 libncurses5
COPY --from=build /usr/local /usr/local
