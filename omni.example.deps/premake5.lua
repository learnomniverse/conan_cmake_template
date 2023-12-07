-- Setup the extension.
local ext = get_current_extension_info()
project_ext(ext)

-- Link folders that should be packaged with the extension.
repo_build.prebuild_link {
    { "data", ext.target_dir.."/data" },
    { "docs", ext.target_dir.."/docs" },
}

-- Build the C++ plugin that will be loaded by the extension.
project_ext_plugin(ext, "omni.example.deps.plugin")
    add_files("include", "include")
    add_files("source", "plugins")
    includedirs {
        "include",
        "plugins/omni.example.deps",
        "%{target_deps}/nv_usd/release/include" }
    libdirs { "%{target_deps}/nv_usd/release/lib" }
    links { "arch", "gf", "sdf", "tf", "usd", "usdGeom", "usdUtils" }
    defines { "NOMINMAX", "NDEBUG" }
    runtime "Release"
    rtti "On"

    filter { "system:linux" }
        exceptionhandling "On"
        staticruntime "Off"
        cppdialect "C++17"
        includedirs { "%{target_deps}/python/include/python3.10" }
        buildoptions { "-D_GLIBCXX_USE_CXX11_ABI=0 -Wno-deprecated-declarations -Wno-deprecated -Wno-unused-variable -pthread -lstdc++fs -Wno-undef" }
        linkoptions { "-Wl,--disable-new-dtags -Wl,-rpath,%{target_deps}/nv_usd/release/lib:%{target_deps}/python/lib:" }
    filter { "system:windows" }
        buildoptions { "/wd4244 /wd4305" }
    filter {}

-- Build Python bindings that will be loaded by the extension.
project_ext_bindings {
    ext = ext,
    project_name = "omni.example.deps.python",
    module = "_example_deps_bindings",
    src = "bindings",
    target_subdir = "omni/example/deps"
}
    includedirs { "include" }
    repo_build.prebuild_link {
        { "python", ext.target_dir.."/omni/example/deps" },
    }
