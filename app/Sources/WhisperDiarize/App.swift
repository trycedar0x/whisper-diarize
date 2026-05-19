import SwiftUI

@main
struct WhisperDiarizeApp: App {
    @StateObject private var runner = TranscriptionRunner()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(runner)
        }
        .windowStyle(.titleBar)
        .windowToolbarStyle(.unified(showsTitle: true))
        .defaultSize(width: 860, height: 620)
        .commands {
            CommandGroup(replacing: .newItem) {}
        }

        Settings {
            SettingsView()
        }
    }
}
