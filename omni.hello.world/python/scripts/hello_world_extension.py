# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
import omni.ext
import omni.usd
from ..bindings._example_carb_bindings import *

# Global public interface object.
_example_carb_interface = None


# Public API.
def get_example_carb_interface() -> IExampleCarbInterface:
    return _example_carb_interface


# Use the extension entry points to acquire and release the interface,
# and to subscribe to usd stage events.
class HelloWorldExtension(omni.ext.IExt):
    def on_startup(self):
        # Acquire the example USD interface.
        global _example_carb_interface
        _example_carb_interface = acquire_example_carb_interface()

        # Print some info about the stage from C++.
        _example_carb_interface.print_stage_info()

    def on_shutdown(self):
        global _example_carb_interface

        # Release the example USD interface.
        release_example_carb_interface(_example_carb_interface)
        _example_carb_interface = None
