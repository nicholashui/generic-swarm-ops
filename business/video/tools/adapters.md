# Video tools

Wave 2 CI stubs (no external media APIs):

| tool_id | Adapter | Human gate |
|---------|---------|------------|
| `video_media_gen_stub` | local fake asset URI | no |
| `video_script_format` | fountain-lite script blob | no |
| `video_qc_stub` | consistency QC pass | no |
| `video_package_stub` | package deliverable | **yes** (DNA step + register) |

Also used on spine: `audit_log_writer`.

Registered in `business/security/tool-permissions/tool-permission-register.json` and `TOOL_ADAPTERS` in `backend/app/infrastructure/tools/adapters.py`.

Future: Sora / Veo / Kling / ElevenLabs with budgets — after stubs.
