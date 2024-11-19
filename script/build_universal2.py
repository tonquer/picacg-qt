import tempfile
import subprocess
import glob
import os
import sys
from wheel_filename import parse_wheel_filename
from delocate import fuse


cwd = "."
class Universal2Bundler:

    def build(self, dest_dir, package):
        with tempfile.TemporaryDirectory() as tmp_dir:

            amd64_binary = "macosx_10_10_x86_64"
            arm64_binary = "macosx_11_0_arm64"
            subprocess.check_call(['python', '-m', 'pip', 'download', '--only-binary=:all:','--no-deps','--platform', amd64_binary, package, '-d', tmp_dir])
            subprocess.check_call(['python', '-m', 'pip', 'download', '--only-binary=:all:','--no-deps','--platform', arm64_binary, package, '-d', tmp_dir])
            universal_wheels = glob.glob("{0}/*".format(tmp_dir))

            wheel = parse_wheel_filename(universal_wheels[0])
            universal2_wheel = os.path.join(dest_dir, "{0}-{1}-{2}-{3}-macosx_10_10_universal2.whl".format(package, wheel.version, wheel.python_tags[0], wheel.abi_tags[0]))
            fuse.fuse_wheels(*universal_wheels, universal2_wheel)
            print("Successfully created universal2 wheel ", universal2_wheel)
# python3 -m pip download --only-binary=:all: --platform macosx_10_10_x86_64 Pillow
# python3 -m pip download --only-binary=:all: --platform macosx_11_0_arm64 Pillow
name = sys.argv[1]
bundler = Universal2Bundler()
#bundler.build(cwd, "pillow")
#bundler.build(cwd, "cffi")
#bundler.build(cwd, "curl_cffi")
bundler.build(cwd, name)