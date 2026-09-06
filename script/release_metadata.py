import os


def build_metadata(event_name, ref, sha):
    """根据触发事件生成版本，手动构建不借用已有标签。"""
    short_sha = sha[:7]
    tag = ref[len("refs/tags/"):] if event_name == "push" and ref.startswith("refs/tags/") else ""
    prefix = "bika_" + tag if tag else "bika_dev_" + short_sha
    return {"PACKAGE_PREFIX": prefix, "TAG_NAME": tag, "HEAD_SHA_SHORT": short_sha}


def main():
    metadata = build_metadata(os.environ["GITHUB_EVENT_NAME"], os.environ["GITHUB_REF"], os.environ["GITHUB_SHA"])
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
        for key, value in metadata.items():
            output.write(f"{key}={value}\n")


if __name__ == "__main__":
    main()
