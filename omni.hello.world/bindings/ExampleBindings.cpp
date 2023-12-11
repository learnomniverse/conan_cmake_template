// Copyright (c) 2022, NVIDIA CORPORATION. All rights reserved.
//
// NVIDIA CORPORATION and its licensors retain all intellectual property
// and proprietary rights in and to this software, related documentation
// and any modifications thereto.  Any use, reproduction, disclosure or
// distribution of this software and related documentation without an express
// license agreement from NVIDIA CORPORATION is strictly prohibited.
//

#include <carb/BindingsPythonUtils.h>

#include <omni/hello/world/IExampleCarbInterface.h>

CARB_BINDINGS("omni.hello.world.python")

DISABLE_PYBIND11_DYNAMIC_CAST(omni::hello::world::IExampleCarbInterface)

namespace {

    // Define the pybind11 module using the same name specified in premake5.lua
    PYBIND11_MODULE(_example_bindings, m) {
        using namespace omni::hello::world;

        m.doc() = "pybind11 omni.hello.world bindings";

        carb::defineInterfaceClass<IExampleCarbInterface>(
            m, "IExampleCarbInterface", "acquire_example_carb_interface", "release_example_carb_interface")
            .def("print_stage_info", &IExampleCarbInterface::printStageInfo)
            /**/;
    }
}
