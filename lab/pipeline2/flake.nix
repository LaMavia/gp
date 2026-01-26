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
          parallel
          snakemake
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
          jupyter
          vl-convert-python
        ]) ++ [
          (pkgs.callPackage ./clann.nix { })
          (pkgs.callPackage ./datasets.nix { })
        ];

        shellHook = ''
          export PATH="/home/mavia/projectes/uni/gp/lab/04/iqtree-3.0.1-Linux/bin:$PATH"
        '';
      };
    }
  );
}
