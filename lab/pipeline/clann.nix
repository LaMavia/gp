{ stdenv
, fetchFromGitHub
, pkgs
,
}:
stdenv.mkDerivation rec {
  pname = "clann";
  version = "v4.2.5";
  rev = "194f8aa";
  src = fetchFromGitHub {
    owner = "ChrisCreevey";
    repo = "clann";
    rev = rev;
    sha256 = "sha256-0MzYgfP5yVcBIYCJf6gb1nVBqS3P4Xlex1N/fOxerKk=";
  };

  nativeBuildInputs = with pkgs; [
    autoreconfHook
  ];

  buildInputs = with pkgs; [ automake116x readline ];

}
