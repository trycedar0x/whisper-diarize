import SwiftUI

struct ErrorView: View {
    @EnvironmentObject private var runner: TranscriptionRunner
    let message: String

    var body: some View {
        VStack(spacing: 20) {
            Image(systemName: "exclamationmark.triangle.fill")
                .font(.system(size: 48))
                .foregroundStyle(.red)

            Text("Transcription Failed")
                .font(.title2.weight(.semibold))

            Text(message)
                .font(.body)
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
                .frame(maxWidth: 400)

            HStack(spacing: 12) {
                Button("Show Log") { runner.state = .running(phase: "") }
                    .buttonStyle(.bordered)
                Button("Try Again") { runner.reset() }
                    .buttonStyle(.borderedProminent)
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .padding(40)
    }
}
