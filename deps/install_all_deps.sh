#!/bin/bash
set -e

SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")

# Check if a Conan profile exists
PROFILE_EXISTS=1
conan profile show &> /dev/null || PROFILE_EXISTS=0

if [ "$PROFILE_EXISTS" -eq 0 ]; then
    # If no profile exists, detect and create one
    echo "No profile exists, creating one with 'conan profile detect'"
    conan profile detect
fi

conan create "$SCRIPT_DIR"/kit_sdk --build=missing
conan create "$SCRIPT_DIR"/nv_usd --build=missing
conan create "$SCRIPT_DIR"/carb_sdk --build=missing
# packman-provided pybind11 is already configured with wrong paths, use a
# from-source one so that we don't insert wrong paths
# conan create "$SCRIPT_DIR"/pybind11 --build=missing
conan create "$SCRIPT_DIR"/python --build=missing

GREEN='\033[0;32m' # ANSI escape code for green text
NC='\033[0m'  # No Color
echo -e "${GREEN}[DONE] all conan dependencies have been created${NC}"
