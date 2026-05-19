// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Minutes",
    platforms: [.macOS(.v14)],
    targets: [
        // Core library — pure logic, no UI, fully testable
        .target(
            name: "MinutesCore",
            path: "Sources/MinutesCore"
        ),

        // Main app — UI layer, depends on Core
        .executableTarget(
            name: "Minutes",
            dependencies: ["MinutesCore"],
            path: "Sources/Minutes",
            resources: [
                .copy("Resources/AppIcon.icns"),
                .copy("Resources/AppIcon.png"),
                .copy("Resources/transcribe.py"),
                .copy("Resources/pyproject.toml"),
                .copy("Resources/uv.lock"),
            ]
        ),

        // Unit tests — run with: swift test
        .testTarget(
            name: "MinutesTests",
            dependencies: ["MinutesCore"],
            path: "Tests/MinutesTests"
        ),

        // UI tests — open app/Package.swift in Xcode and press ⌘U to run
        // (excluded from swift test: requires a running app and Xcode scheme)
    ]
)
