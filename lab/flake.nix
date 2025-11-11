{
  inputs = {
    utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "nixpkgs/nixos-unstable";
  };
  outputs = { self, nixpkgs, utils }: utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShell = pkgs.mkShell {
        buildInputs = with pkgs; [
          (rWrapper.override
            { packages = with rPackages; [ TreeDist languageserver ]; })
          muscle
        ] ++ (with python313Packages; [
          python
          biopython
          matplotlib
          tqdm
          numpy
        ]);
      };
    }
  );
}
