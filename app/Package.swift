// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "WhisperDiarize",
    platforms: [.macOS(.v14)],
    targets: [
        .executableTarget(
            name: "WhisperDiarize",
            path: "Sources/WhisperDiarize",
            resources: [
                .copy("Resources/transcribe.py"),
                .copy("Resources/pyproject.toml"),
                .copy("Resources/uv.lock"),
            ]
        )
    ]
)
