# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

# [0.11.0] - 2025-06-22

### Added

-   Various colouring styles, see [Style](https://github.com/onyx-and-iris/slobs-cli/tree/main?tab=readme-ov-file#style)
    -   colouring is applied to list tables as well as highlighted information in stdout/stderr output.
    -   table border styling may be optionally disabled with the --no-border flag.

# [0.10.0] - 2025-06-13

### Changed

-   scene commands are prone to raise ProtocolErrors if called too quickly in succession. To make these errors a little more user friendly the following changes have been made:
    -   They print error messages to stderr
    -   They return exit code 2

# [0.9.0] - 2025-06-12

### Added

-   scenecollection command group, see [Scene Collection](https://github.com/onyx-and-iris/slobs-cli/tree/main?tab=readme-ov-file#scene-collection)
-   add audio status commmand.

# [0.8.4] - 2025-06-12

### Added

-   custom error class SlobsCliError.
-   scene switch command: if the --preview flag is not passed and we're in studio mode then write a message to the user to indicate the transition is being forced.

### Changed

-   scene list now shows which scene is the current active scene.
-   audio list now shows mute states.
-   scene list and audio list commands now print as tables
-   --id option added to scene and audio commands to show the source ID in the output
    -   by default this is no longer displayed

-   erroneous paths now print error messages and return 1 instead of raising exceptions.
    -   unit tests updated to reflect the changes.

# [0.7.6] - 2025-06-11

### Added

-   --version/-v command.

### Changed

-   --token/-t is now required.

# [0.7.3] - 2025-06-10

### Added

-   Initial release.