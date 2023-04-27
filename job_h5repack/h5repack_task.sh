#!/usr/bin/env bash
set -e

export HDF5_PLUGIN_PATH=/opt/conda/lib/python3.10/site-packages/braingeneers/data/mxw_h5_plugin/Linux/

while true; do
  export FILE=$(python get_task.py)
  export BASE_DIR=$(dirname ${FILE})
  export BASE_FILE=$(basename ${FILE})
  export ROWMAJOR_FILE="${BASE_FILE%%.*}.rowmajor.h5"

  if [ "${FILE}" == "END" ]; then break; fi

  aws --endpoint ${ENDPOINT} s3 cp "${FILE}" "/tmp/"
  h5repack -v -l "/data_store/data0000/groups/routed/raw:CHUNK=1x30000" -i "/tmp/${BASE_FILE}" -o "/tmp/${ROWMAJOR_FILE}"
  aws --endpoint ${ENDPOINT} s3 cp "/tmp/${BASE_FILE%%.*}.rowmajor.h5" "${BASE_DIR}/"
  # todo delete old file, currently not implemented for safety during testing phase
  # python update_metadata.py  # todo add after testing
  rm tmp/${BASE_FILE}
done