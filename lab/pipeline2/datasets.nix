{ stdenv
, fetchurl
, pkgs
,
}:
stdenv.mkDerivation rec {
  pname = "datasets";
  version = "v2.1";
  src = fetchurl {
    url = "https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/v2/linux-amd64/datasets";
    hash = "sha256-qIEPCumNT9MjESl0EnESPpJbS4YtqNx0At9HqD2Dja0=";
  };

  phases = [ "installPhase" ]; # Removes all phases except installPhase

  installPhase = ''
    mkdir -p $out/bin
    cp $src $out/bin/datasets
    chmod +x $out/bin/datasets
  '';
}
