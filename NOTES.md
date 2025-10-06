Frontend build & environment notes

- If you see warnings like "script ... is installed in '...\LocalCache\local-packages\Python313\Scripts' which is not on PATH", add that Scripts folder to your PATH so pip-installed CLI scripts (uvicorn, fastapi, watchfiles, etc.) are available. Example PowerShell command:

  $env:Path += ";$env:LOCALAPPDATA\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts"

  To persist this across sessions, add it through System Properties > Environment Variables or use [Microsoft docs].

- Frontend build prerequisites:
  - Install Node.js (which includes npm). Verify with `node -v` and `npm -v`.
  - From repository root run: `cd frontend; npm install; npm run build`.

- If `npm install` previously failed due to tailwind version resolution, we've pinned `tailwindcss` to `^3.4.7` in `frontend/package.json` which is a known stable release. If you still see errors, try clearing npm cache:

  npm cache clean --force

  then re-run `npm install`.

- Packaging: `scripts/build_all.ps1` will skip frontend build if npm isn't found and still create `axiom-v1.0.zip` with textual artifacts.
