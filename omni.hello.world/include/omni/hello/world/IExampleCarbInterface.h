// Copyright (c) 2022, NVIDIA CORPORATION. All rights reserved.
//
// NVIDIA CORPORATION and its licensors retain all intellectual property
// and proprietary rights in and to this software, related documentation
// and any modifications thereto.  Any use, reproduction, disclosure or
// distribution of this software and related documentation without an express
// license agreement from NVIDIA CORPORATION is strictly prohibited.
//
#pragma once

#include <carb/Interface.h>

namespace omni {
    namespace hello {
        namespace world {

            /**
             * Interface used to interact with the example C++ USD plugin from Python.
             */
            class IExampleCarbInterface {
            public:
                /// @private
                CARB_PLUGIN_INTERFACE("omni::hello::world::IExampleCarbInterface", 1, 0);

                /**
                 * Instructs the C++ module to use a stage for the next calls.
                 */
                virtual void setStageFromStageId(long stageId) = 0;

                /**
                 * Print some info about the currently open USD stage from C++.
                 */
                virtual void printStageInfo() const = 0;
            };

        }
    }
}
