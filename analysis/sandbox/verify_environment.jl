using Pkg, TOML, Test
VERSION == v"1.13.1" || error("Julia 1.13.1 required")
get(ENV,"JULIA_LOAD_PATH","")=="@:@stdlib" || error("shared LOAD_PATH")
expected=Set(["Test","LinearAlgebra","Random","Statistics"])
project=TOML.parsefile(Base.active_project())
@test Set(keys(project["deps"]))==expected
stdlibs=Pkg.Types.stdlibs()
# Statistics is an upgradable stdlib resolved from the registry on Julia 1.13;
# allow its declared UUID, rather than admitting arbitrary registry packages.
statistics_uuid=Base.UUID(project["deps"]["Statistics"])
@test all(uuid in keys(stdlibs) || uuid==statistics_uuid for uuid in keys(Pkg.dependencies()))
@test_throws ArgumentError Base.require(Main,:Turing)
@test_throws ArgumentError Base.require(Main,:Metal)
println("environment verified: ",Base.active_project()," Julia ",VERSION," LOAD_PATH=",LOAD_PATH)
