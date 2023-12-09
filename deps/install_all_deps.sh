#!/bin/bash
set -e

SCRIPT_DIR=$(dirname "${BASH_SOURCE}")

conan create "$SCRIPT_DIR"/kit_sdk --update
conan create "$SCRIPT_DIR"/nv_usd --update
echo "[DONE] all conan dependencies have been created"
