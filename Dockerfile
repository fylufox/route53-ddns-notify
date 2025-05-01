# ベースイメージとしてAmazon Linux 2を使用
FROM amazonlinux:2023

# 必要なツールをインストール
RUN yum update -y && \
    yum install -y \
        docker \
        python3 \
        python3-pip \
        zip \
        tar \
        git \
        unzip && \
    yum clean all

# AWS CLIとAWS SAM CLIをインストール
RUN pip3 install --no-cache-dir aws-sam-cli

RUN yum install -y awscli

# 作業ディレクトリを設定
WORKDIR /app

# コンテナ起動時のデフォルトコマンド
CMD ["/bin/bash"]