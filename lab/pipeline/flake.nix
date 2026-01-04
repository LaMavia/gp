{
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, utils }: utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShell = pkgs.mkShell {
        buildInputs = with pkgs; [
          mmseqs2
          cd-hit
          (rWrapper.override
            { packages = with rPackages; [ TreeDist languageserver ggtree treeio Signac ]; })
          muscle
        ] ++ (with python313Packages; [
          python
          biopython
          altair
          tqdm
          numpy
          requests
          ruff
        ]);
      };
    }
  );
}
