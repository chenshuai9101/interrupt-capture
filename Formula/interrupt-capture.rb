class InterruptCapture < Formula
  include Language::Python::Shebang

  desc "Local plain-text CLI to capture & resume what you were doing when interrupted"
  homepage "https://github.com/muyunye/interrupt-capture"
  url "file:///tmp/interrupt-capture-0.1.0.tar.gz"
  sha256 "636830f9d9f681dbe5957dafa1d13a01a211f50815e537e3947da036c652a127"
  version "0.1.0"
  license "MIT"

  depends_on "python@3.12"

  def install
    # stdlib-only script; pin its shebang to the Homebrew python then install as `ic`
    rewrite_shebang detected_python_shebang, "interrupt_capture.py"
    bin.install "interrupt_capture.py" => "ic"
  end

  test do
    assert_match "Interrupt Capture", shell_output("#{bin}/ic --help")
    ENV["HOME"] = testpath
    system bin/"ic", "smoke test note"
    assert_match "smoke test note", shell_output("#{bin}/ic resume")
  end
end
