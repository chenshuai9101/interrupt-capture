class InterruptCapture < Formula
  include Language::Python::Shebang

  desc "Local plain-text CLI to capture & resume what you were doing when interrupted"
  homepage "https://github.com/chenshuai9101/interrupt-capture"
  url "file:///tmp/interrupt-capture-0.2.0.tar.gz"
  sha256 "67dc18ba265eafa061c99e1a610c3c5018a6959013c668cbbab82a300b29fd51"
  version "0.2.0"
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
