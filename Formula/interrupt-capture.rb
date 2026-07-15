class InterruptCapture < Formula
  include Language::Python::Shebang

  desc "Local plain-text CLI to capture & resume what you were doing when interrupted"
  homepage "https://github.com/chenshuai9101/interrupt-capture"
  url "https://github.com/chenshuai9101/interrupt-capture/archive/refs/tags/v0.3.1.tar.gz"
  sha256 "7c9da909e8eb7e94c38dd3753687bc4e401dd4ab78240fb4dbc7777a67849061"
  version "0.3.1"
  license "MIT"

  depends_on "python@3.12"

  def install
    # stdlib-only script; pin its shebang to the Homebrew python then install as `ic`
    rewrite_shebang detected_python_shebang, "interrupt_capture.py"
    bin.install "interrupt_capture.py" => "ic"
    pkgshare.install "assets"
  end

  test do
    assert_match "Interrupt Capture", shell_output("#{bin}/ic --help")
    ENV["HOME"] = testpath
    system bin/"ic", "smoke test note"
    assert_match "smoke test note", shell_output("#{bin}/ic resume")
  end
end
