// Copyright (c) 2023, NVIDIA CORPORATION. All rights reserved.
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
#include <omni/timeline/ITimeline.h>
#include <omni/timeline/TimelineTypes.h>

#include <pxr/usd/usd/notice.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usd/stageCache.h>
#include <pxr/usd/usd/primRange.h>
#include <pxr/usd/usdGeom/metrics.h>
#include <pxr/usd/usdGeom/xform.h>
#include <pxr/usd/usdUtils/stageCache.h>

const struct carb::PluginImplDesc pluginImplDesc = { "omni.hello.world.plugin",
                                                     "An example hello world C++ extension.", "NVIDIA",
                                                     carb::PluginHotReload::eEnabled, "dev" };

namespace omni {
    namespace hello {
        namespace world {

            class ExampleExtension : public IExampleCarbInterface, public PXR_NS::TfWeakBase {
            public:

                void setStageFromStageId(long stageId) override {
                    if (stageId) {
                        m_stage = PXR_NS::UsdUtilsStageCache::Get().Find(PXR_NS::UsdStageCache::Id::FromLongInt(stageId));
                    }
                }

                void printStageInfo() const override {

                    if (!m_stage) {
                        return;
                    }

                    CARB_LOG_WARN("---Stage Info Begin---\n");

                    // Print the USD stage's up-axis.
                    const PXR_NS::TfToken stageUpAxis = PXR_NS::UsdGeomGetStageUpAxis(m_stage);
                    CARB_LOG_WARN("Stage up-axis is: %s.\n", stageUpAxis.GetText());

                    // Print the USD stage's meters per unit.
                    const double metersPerUnit = PXR_NS::UsdGeomGetStageMetersPerUnit(m_stage);
                    CARB_LOG_WARN("Stage meters per unit: %f.\n", metersPerUnit);

                    // Print the USD stage's prims.
                    const PXR_NS::UsdPrimRange primRange = m_stage->Traverse();
                    for (const PXR_NS::UsdPrim& prim : primRange) {
                        CARB_LOG_WARN("Stage contains prim: %s.\n", prim.GetPath().GetString().c_str());
                    }

                    CARB_LOG_WARN("---Stage Info End---\n\n");
                }
            private:
                PXR_NS::UsdStageRefPtr m_stage;
            };

        }
    }
}

CARB_PLUGIN_IMPL(pluginImplDesc, omni::hello::world::ExampleExtension)

void fillInterface(omni::hello::world::ExampleExtension& iface) {
}
