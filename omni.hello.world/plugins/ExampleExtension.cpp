// Copyright (c) 2022, NVIDIA CORPORATION. All rights reserved.
//
// NVIDIA CORPORATION and its licensors retain all intellectual property
// and proprietary rights in and to this software, related documentation
// and any modifications thereto.  Any use, reproduction, disclosure or
// distribution of this software and related documentation without an express
// license agreement from NVIDIA CORPORATION is strictly prohibited.
//

#define CARB_EXPORTS

#include <carb/PluginUtils.h>

#include <omni/hello/world/IExampleCarbInterface.h>
#include <omni/ext/ExtensionsUtils.h>
#include <omni/ext/IExt.h>
#include <omni/kit/IApp.h>
// #include <omni/timeline/ITimeline.h>
// #include <omni/timeline/TimelineTypes.h>

// #include <pxr/usd/usd/notice.h>
// #include <pxr/usd/usd/stage.h>
// #include <pxr/usd/usd/stageCache.h>
// #include <pxr/usd/usd/primRange.h>
// #include <pxr/usd/usdGeom/metrics.h>
// #include <pxr/usd/usdGeom/xform.h>
// #include <pxr/usd/usdUtils/stageCache.h>

// #include <vector>

const struct carb::PluginImplDesc pluginImplDesc = { "omni.hello.world.plugin",
                                                     "An example hello world C++ extension.", "NVIDIA",
                                                     carb::PluginHotReload::eEnabled, "dev" };

namespace omni {
    namespace hello {
        namespace world {

            class ExampleExtension : public IExampleCarbInterface {
            public:

                void printStageInfo() const override {
                    CARB_LOG_ERROR("YEAH printStageInfo()!!!!!!!");
                }
            };

        }
    }
}

CARB_PLUGIN_IMPL(pluginImplDesc, omni::hello::world::ExampleExtension)

void fillInterface(omni::hello::world::ExampleExtension& iface) {
}
