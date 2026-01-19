{
  inputs = {
    utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "nixpkgs/nixos-unstable";
  };
  outputs = { self, nixpkgs, utils }: utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
      lib = nixpkgs.lib;

    in
    {
      devShell = pkgs.mkShell rec {
        buildInputs = with pkgs; [
          mmseqs2
          cd-hit
          (rWrapper.override
            { packages = with rPackages; [ TreeDist languageserver ggtree treeio ]; })
          muscle
          raxml
          veryfasttree
          jdk
          libxext
        ] ++ (with python313Packages; [
          python
          biopython
          matplotlib
          tqdm
          numpy
          requests
        ]);

        CPATH = builtins.concatStringsSep ":" [
          (lib.makeSearchPathOutput "dev" "include" [ pkgs.libxext ])
        ];
        #
        # makeFlags = [
        #   "USE_PGXS=1"
        # ];

        shellHook = ''
          # Augment the dynamic linker path
          export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:${CPATH}"
          export LIBCLANG_PATH="${pkgs.libclang.lib}/lib";
          export PGDATA=$(realpath ./pg_data)
          export PATH="$(realpath ./result/bin):$PATH"
        '';

      };
    }
  );
}
