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
import carb

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

        # Subscribe to omni.usd stage events so we can inform the C++ plugin when a new stage opens.
        usd_context = omni.usd.get_context()
        self._stage_event_sub = usd_context.get_stage_event_stream().create_subscription_to_pop(
            self._on_stage_event, name="omni.example.cpp.usd"
        )

    def on_shutdown(self):
        global _example_carb_interface

        # Unsubscribe from omni.usd stage events.
        self._stage_event_sub = None

        # Release the example USD interface.
        release_example_carb_interface(_example_carb_interface)
        _example_carb_interface = None

    def _on_stage_event(self, event):
        if event.type == int(omni.usd.StageEventType.OPENED):
            _example_carb_interface.set_stage_from_stage_id(omni.usd.get_context().get_stage_id())
            # Print some info about the stage from C++
            _example_carb_interface.print_stage_info()
        elif event.type == int(omni.usd.StageEventType.CLOSED):
            _example_carb_interface.set_stage_from_stage_id(0)
