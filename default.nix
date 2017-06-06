{ pkgs ? import <nixpkgs> {} }:
with pkgs.python3Packages;
let
  inp = [
    python
    requests
    docopt
  ];
in buildPythonPackage {
  name = "radioactive-2017-06-06";
  src = ./.;
  buildInputs = inp;
}
