FROM ubuntu:focal

ENV TZ=Europe/Rome

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update \
	&& DEBIAN_FRONTEND=noninteractive apt upgrade -y \
	&& apt install -y \
		apt-utils \
		debhelper \
		python3 \
		python3-dev \
		python3-pip \
		python3-setuptools \
		libxml2-dev \
		zlib1g-dev \
		build-essential \
		lintian \
		devscripts \
		git \
		ruby-full \
		bash-completion

RUN gem install ronn-ng

COPY dput.cf /root/.dput.cf

WORKDIR /opt

ENV RUBYOPT="-KU -E utf-8:utf-8"

WORKDIR /opt/kathara/scripts/Linux
