#!/bin/bash
set -e

SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")

conan create "$SCRIPT_DIR"/kit_sdk --build=missing
conan create "$SCRIPT_DIR"/nv_usd --build=missing
conan create "$SCRIPT_DIR"/carb_sdk --build=missing
conan create "$SCRIPT_DIR"/pybind11 --build=missing
conan create "$SCRIPT_DIR"/python --build=missing

GREEN='\033[0;32m' # ANSI escape code for green text
NC='\033[0m'  # No Color
echo -e "${GREEN}[DONE] all conan dependencies have been created${NC}"

