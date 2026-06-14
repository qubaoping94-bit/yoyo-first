# GitHub Upload

Target repository:

```text
https://github.com/qubaoping94-bit/yoyo-first
```

Recommended upload flow:

```powershell
git clone https://github.com/qubaoping94-bit/yoyo-first.git <clean-upload-dir>
Copy-Item -Recurse -Force .\skill-packs <clean-upload-dir>\
git -C <clean-upload-dir> status --short
git -C <clean-upload-dir> add skill-packs
git -C <clean-upload-dir> commit -m "Add Youyou special demo delivery skill pack"
git -C <clean-upload-dir> push origin main
```

If credentialed push fails, keep the prepared clone and upload the `skill-packs/youyou-special-demo-delivery-pipeline` folder manually through GitHub Desktop or the web UI.

