FROM braingeneers/braingeneers:latest

RUN python -m pip install \
    pyyaml  \
    stream_zip

WORKDIR /s3_glacier_backup
COPY src /s3_glacier_backup/
