# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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